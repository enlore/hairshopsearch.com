from flask import (Blueprint, render_template, current_app, redirect, url_for,
    flash, request, jsonify)
from flask.ext.security import current_user, login_required

from sqlalchemy import or_

from ..user.forms import (AddressForm, HoursForm, BioForm, PaymentsForm,
    MenuItemForm, RemoveItemForm, PhotoForm, SocialMediaForm,
    NewProviderForm, NewConsumerForm, HairInfoForm, ProductForm,
    RoutineForm)
from ..forms import ConsumerDashForm, ProviderDashForm, MenuItemForm, FileUploadForm

from ..models import (Gallery, Photo, Product)
from ..provider.models import (Provider, Menu, MenuItem, ProviderInstance,
    Address, Hours, Location)
from ..consumer.models import (Consumer, ConsumerInstance, HairRoutine)

from ..core import db
from ..helpers import acceptable_url_string, put_s3, process_img, delete_from_s3
from ..indexer import indexer

from datetime import datetime, timedelta

import base64
import hmac
import hashlib
import json
import os

dashboard = Blueprint('dashboard', __name__,
        url_prefix='/dashboard', template_folder='templates')


@dashboard.route('/photo/<int:id>/delete')
def delete_photo(id):
    photo = Photo.query.get(id)
    current_app.logger.info(photo.url)

    delete_from_s3(photo.url)
    delete_from_s3(photo.lg_thumb)
    delete_from_s3(photo.sm_thumb)

    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('.profile'))


@dashboard.route('/avatar/save', methods=['POST'])
def save_avatar():
    entity = current_user.provider or current_user.consumer

    form = FileUploadForm()

    if form.validate_on_submit():
        s3_keys = process_img(form.up_file.data)

        current_app.logger.info(s3_keys)
        entity.avatar = Photo(
            url=s3_keys['original'],
            sm_thumb=s3_keys['sm_thumb'],
            lg_thumb=s3_keys['lg_thumb']
            )

        db.session.add(entity)
        db.session.commit()
    return redirect(url_for('dashboard.profile'))


@dashboard.route('/photo/save', methods=['POST'])
def save_photo():
    entity = current_user.provider or current_user.consumer

    if not entity.gallery:
        entity.gallery = Gallery()
    
    form = FileUploadForm()

    if form.validate_on_submit():
        current_app.logger.info(form.up_file.data)
        s3_keys = process_img(form.up_file.data)

        entity.gallery.photos.append(Photo(
            url=s3_keys['original'],
            sm_thumb=s3_keys['sm_thumb'],
            lg_thumb=s3_keys['lg_thumb']
            ))

        db.session.add(entity)
        db.session.commit()

    return redirect(url_for('dashboard.profile'))

@dashboard.route('/menu/add', methods=['POST'])
@login_required
def save_menu_item():
    current_app.logger.info(request.form)
    p = current_user.provider

    # if menu_type already exists, append thing to it's items
    # if not, create it and then append thing to it's items
    menu_item = MenuItem(
           name=request.form['name'],
           price=request.form['price'],
           description=request.form['description']
    )

    got_it = False

    for menu in p.menus:
        if menu.menu_type == request.form['menu_type']:
            got_it = True
            menu.menu_items.append(menu_item)
     
    if not got_it:
        menu = Menu(menu_type=request.form['menu_type']) 
        p.menus.append(menu)
        p.menu.menu_items.append(item)

    db.session.add(p)
    db.session.commit()
    return redirect(url_for('.profile'))

@dashboard.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    rm_menu_item_form = RemoveItemForm()

    if current_user.consumer:
        consumer = current_user.consumer

        if not consumer.hair_routine:
            consumer.hair_routine = HairRoutine()

        form = ConsumerDashForm()

        if not form.validate_on_submit():
            if form.errors:
                flash(form.errors, 'error')

        else:
            consumer.user.first_name    = form.first_name.data
            consumer.user.last_name     = form.last_name.data
            consumer.user.email         = form.email.data
            consumer.user.birth_day     = form.birth_day.data
            consumer.user.gender        = form.gender.data
            consumer.location           = form.location.data

            consumer.hair_routine.hair_condition        = ' '.join(form.hair_condition.data)
            consumer.hair_routine.scalp_condition       = ' '.join(form.scalp_condition.data)

            consumer.hair_routine.chemical_treat        = form.treat.data
            consumer.hair_routine.last_treatment        = form.last_treat.data
            consumer.hair_routine.fav_style             = form.fav_style.data
            consumer.hair_routine.shampoo_type          = form.shampoo.data
            consumer.hair_routine.shampoo_frequency     = form.shampoo_freq.data
            consumer.hair_routine.conditioner_type      = form.conditioner.data
            consumer.hair_routine.condition_frequency   = form.condition_freq.data
            consumer.hair_routine.last_trim             = form.trim_last.data

            consumer.blog_url           = form.blog_url.data
            consumer.fb_url             = form.facebook_url.data
            consumer.gplus_url          = form.google_plus_url.data
            consumer.youtube_url        = form.youtube_url.data
            #consumer.vimeo_url         = form.vimeo_url.data
            #consumer.other_url         = form.other_url.data

            db.session.add(consumer)
            db.session.commit()

            return redirect(url_for('dashboard.profile'))

        if not consumer.hair_routine:
            consumer.hair_routine = HairRoutine()

        form.first_name.data    = consumer.user.first_name
        form.last_name.data     = consumer.user.last_name
        form.email.data         = consumer.user.email
        form.gender.data        = consumer.user.gender or 'rather_not'
        form.birth_day.data     = consumer.user.birth_day

        form.location.data          = consumer.location

        if not consumer.hair_routine.hair_condition:
            consumer.hair_routine.hair_condition = 'none'

        form.hair_condition.data    = consumer.hair_routine.hair_condition.split(' ')

        if not consumer.hair_routine.scalp_condition:
            consumer.hair_routine.scalp_condition = 'none'

        form.scalp_condition.data   = consumer.hair_routine.scalp_condition.split(' ')

        form.treat.data             = consumer.hair_routine.chemical_treat
        form.last_treat.data        = consumer.hair_routine.last_treatment
        form.fav_style.data         = consumer.hair_routine.fav_style
        form.shampoo.data           = consumer.hair_routine.shampoo_type
        form.shampoo_freq.data      = consumer.hair_routine.shampoo_frequency
        form.conditioner.data       = consumer.hair_routine.conditioner_type
        form.condition_freq.data    = consumer.hair_routine.condition_frequency
        form.trim_last.data         = consumer.hair_routine.last_trim
        form.facebook_url.data      = consumer.fb_url
        form.google_plus_url.data   = consumer.gplus_url
        form.blog_url.data          = consumer.blog_url
        form.youtube_url.data       = consumer.youtube_url

        return render_template('dashboard/consumer.html',
                avatar_upload_form=FileUploadForm(),
                gallery_upload_form=FileUploadForm(),
                consumer=current_user.consumer,
                form=form)

    # TODO: use /profile as a redirect to entity specific route
    if current_user.provider:
        provider = current_user.provider

        form = ProviderDashForm()
        menu_form = MenuItemForm()

        if not form.validate_on_submit():
            if form.errors:
                flash(form.errors, 'error')

        else:
            #acceptable_url_string()
            provider.business_name  = form.business_name.data
            provider.business_url   = acceptable_url_string(
                form.business_name.data,
                current_app.config['ACCEPTABLE_URL_CHARS']
                    )
            provider.email          = form.email.data
            provider.phone          = form.phone.data

            provider.payment_methods = ' '.join(form.payment_methods.data)
            current_app.logger.info(provider.payment_methods)

            provider.address.street_1   = form.street_1.data
            provider.address.street_2   = form.street_2.data
            provider.address.city       = form.city.data
            provider.address.state      = form.state.data
            provider.address.zip_code   = form.zip_code.data

            provider.bio            = form.bio.data
            provider.fb_url         = form.fb_url.data
            provider.twitter_url    = form.twitter_url.data

            provider.hours.monday_open      = form.monday_open.data
            provider.hours.monday_close     = form.monday_close.data
            provider.hours.tuesday_open     = form.tuesday_open.data
            provider.hours.tuesday_close    = form.tuesday_close.data
            provider.hours.wednesday_open   = form.wednesday_open.data
            provider.hours.wednesday_close  = form.wednesday_close.data
            provider.hours.thursday_open    = form.thursday_open.data
            provider.hours.thursday_close   = form.thursday_close.data
            provider.hours.friday_open      = form.friday_open.data
            provider.hours.friday_close     = form.friday_close.data
            provider.hours.saturday_open    = form.saturday_open.data
            provider.hours.saturday_close   = form.saturday_close.data
            provider.hours.sunday_open      = form.sunday_open.data
            provider.hours.sunday_close     = form.sunday_close.data

            provider.save()

            return redirect(url_for('dashboard.profile'))

        form.email.data           = provider.email
        form.business_name.data   = provider.business_name
        form.phone.data           = provider.phone
        form.payment_methods.data = provider.payment_methods

        form.street_1.data        = provider.address.street_1
        form.street_2.data        = provider.address.street_2
        form.city.data            = provider.address.city
        form.state.data           = provider.address.state
        form.zip_code.data        = provider.address.zip_code

        form.bio.data             = provider.bio
        form.fb_url.data          = provider.fb_url
        form.twitter_url.data     = provider.twitter_url

        form.monday_open.data     = provider.hours.monday_open
        form.monday_close.data    = provider.hours.monday_close
        form.tuesday_open.data    = provider.hours.tuesday_open
        form.tuesday_close.data   = provider.hours.tuesday_close
        form.wednesday_open.data  = provider.hours.wednesday_open
        form.wednesday_close.data = provider.hours.wednesday_close
        form.thursday_open.data   = provider.hours.thursday_open
        form.thursday_close.data  = provider.hours.thursday_close
        form.friday_open.data     = provider.hours.friday_open
        form.friday_close.data    = provider.hours.friday_close
        form.saturday_open.data   = provider.hours.saturday_open
        form.saturday_close.data  = provider.hours.saturday_close
        form.sunday_open.data     = provider.hours.sunday_open
        form.sunday_close.data    = provider.hours.sunday_close

        gallery_upload_form = FileUploadForm()
        avatar_upload_form = FileUploadForm()
        return render_template('dashboard/provider.html',
                form=form,
                menu_form=menu_form,
                provider=current_user.provider,
                rm_menu_item_form=rm_menu_item_form,
                avatar_upload_form=avatar_upload_form,
                gallery_upload_form=gallery_upload_form)

    return redirect(url_for('frontend.welcome'))

@dashboard.route('/provider/new', methods=['GET', 'POST'])
@login_required
def new_provider():
    form = NewProviderForm()
    if form.validate_on_submit():
        provider = Provider(user=current_user)

        provider.business_name = form.business_name.data

        dirty_name = provider.business_name
        # lower dirty name
        clean_name = acceptable_url_string(dirty_name.lower(),
                current_app.config['ACCEPTABLE_URL_CHARS'])

        pi = ProviderInstance.query.get(clean_name)

        if pi:
            provider.business_url = '{}.{}'.format(clean_name, pi.count)
            pi.count += 1

        else:
            pi = ProviderInstance()
            pi.name = clean_name
            pi.count = 1
            provider.business_url = clean_name

        provider.save()

        db.session.add(pi)
        db.session.commit()

        resp = indexer.index_one(provider, provider.id)
        current_app.logger.info('indexed: {}'.format(resp))

        return redirect(url_for('dashboard.profile'))
    return render_template('dashboard/new_provider.html', form=form)

@dashboard.route('/consumer/new', methods=['GET', 'POST'])
@login_required
def new_consumer():
    form = NewConsumerForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data

        consumer = Consumer(user=current_user)
        # if instance keyed by FirstnameLastname in ConsumerInstance
        # update count by one

        dirty_name = '{}{}'.format(current_user.first_name, current_user.last_name)
        clean_name = acceptable_url_string(dirty_name.lower(),
                current_app.config['ACCEPTABLE_URL_CHARS'])


        ci = ConsumerInstance.query.get(clean_name)

        if ci:
            consumer.consumer_url = '{}.{}'.format(clean_name, ci.count)
            ci.count += 1

        else:
            ci = ConsumerInstance()
            ci.name = clean_name
            ci.count = 1
            consumer.consumer_url = clean_name


        db.session.add(ci)
        db.session.add(consumer)
        db.session.commit()
        return redirect(url_for('dashboard.profile'))
    return render_template('dashboard/new_consumer.html', form=form)
