from flask import (Blueprint, render_template, current_app, redirect, url_for,
    flash, request, jsonify)
from flask.ext.security import current_user, login_required

from sqlalchemy import or_

from ..user.forms import NewProviderForm, NewConsumerForm, RemoveItemForm
from ..forms import (ConsumerDashForm, ProviderDashForm, MenuItemForm,
    FileUploadForm, AddressForm, HoursForm)

from ..models import (Gallery, Photo, Product)
from ..provider.models import (Provider, Menu, MenuItem, ProviderInstance,
    Address, Hours, Location)
from ..consumer.models import (Consumer, ConsumerInstance, HairRoutine)

from ..core import db, HSSError
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
@login_required
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
@login_required
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
@login_required
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

@dashboard.route('/provider/menu/add', methods=['POST'])
@login_required
def save_menu_item():
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
        menu.menu_items.append(menu_item)
        p.menus.append(menu)

    p.save()
    p.index()

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
    # or something, jesus
    if current_user.provider:
        provider = current_user.provider

        form = ProviderDashForm()
        menu_form = MenuItemForm()

        if not form.validate_on_submit():
            if form.errors:
                flash(form.errors, 'error')

        else:
            provider.business_name  = form.business_name.data
            provider.email          = form.email.data
            provider.phone          = form.phone.data

            provider.payment_methods = ' '.join(form.payment_methods.data)

            provider.bio            = form.bio.data
            provider.fb_url         = form.fb_url.data
            provider.twitter_url    = form.twitter_url.data

            provider.save()

            return redirect(url_for('dashboard.profile'))


        form.email.data           = provider.email
        form.business_name.data   = provider.business_name
        form.phone.data           = provider.phone
        form.payment_methods.data = provider.payment_methods

        form.bio.data             = provider.bio
        form.fb_url.data          = provider.fb_url
        form.twitter_url.data     = provider.twitter_url

        address_form = AddressForm(obj=provider.address)
        hours_form = HoursForm(obj=provider.hours)
        gallery_upload_form = FileUploadForm()
        avatar_upload_form = FileUploadForm()

        return render_template('dashboard/provider.html',
                provider=current_user.provider,
                form=form,
                hours_form=hours_form,
                menu_form=menu_form,
                address_form=address_form,
                rm_menu_item_form=rm_menu_item_form,
                avatar_upload_form=avatar_upload_form,
                gallery_upload_form=gallery_upload_form)

    return redirect(url_for('frontend.welcome'))

@dashboard.route('/provider/hours', methods=['POST'])
@login_required
def save_provider_hours():
    provider = current_user.provider
    hours_form = HoursForm()

    provider.hours.monday_open      = hours_form.monday_open.data
    provider.hours.monday_close     = hours_form.monday_close.data
    provider.hours.tuesday_open     = hours_form.tuesday_open.data
    provider.hours.tuesday_close    = hours_form.tuesday_close.data
    provider.hours.wednesday_open   = hours_form.wednesday_open.data
    provider.hours.wednesday_close  = hours_form.wednesday_close.data
    provider.hours.thursday_open    = hours_form.thursday_open.data
    provider.hours.thursday_close   = hours_form.thursday_close.data
    provider.hours.friday_open      = hours_form.friday_open.data
    provider.hours.friday_close     = hours_form.friday_close.data
    provider.hours.saturday_open    = hours_form.saturday_open.data
    provider.hours.saturday_close   = hours_form.saturday_close.data
    provider.hours.sunday_open      = hours_form.sunday_open.data
    provider.hours.sunday_close     = hours_form.sunday_close.data

    provider.save()
    return redirect(url_for('dashboard.profile'))


@dashboard.route('/provider/new', methods=['GET', 'POST'])
@login_required
def new_provider():
    form = NewProviderForm()
    if form.validate_on_submit():
        provider = Provider(user=current_user)

        provider.business_name = form.business_name.data

        provider.save()
        provider.index()

        db.session.add(pi)
        db.session.commit()

        return redirect(url_for('dashboard.new_address'))
    return render_template('dashboard/new_provider.jade', form=form)

@dashboard.route('/provider/address/save', methods=['POST'])
@login_required
def save_provider_address():
    provider = current_user.provider
    address_form = AddressForm()
    if not address_form.validate_on_submit():
        if address_form.errors:
            flash(form.errors, 'error')
            current_app.logger.info(form.errors)

    else:
        provider.address.street_1   = address_form.street_1.data
        provider.address.street_2   = address_form.street_2.data
        provider.address.city       = address_form.city.data
        provider.address.state      = address_form.state.data
        provider.address.zip_code   = address_form.zip_code.data

        lat, lon = provider.address.geocode()[0]
        current_app.logger.info('{}, {}'.format(lat, lon))
        provider.location = Location(lat, lon)

        provider.update_index()
        provider.save()

    return redirect(url_for('dashboard.profile'))

@dashboard.route('/provider/hours/new', methods=['GET', 'POST'])
@login_required
def new_hours():
    provider = current_user.provider
    form = HoursForm(obj=provider.hours)

    if not form.validate_on_submit():
        if form.errors:
            flash(form.errors, 'error')
            current_app.logger.info(form.errors)

    else:
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

        return redirect(url_for('dashboard.new_menus'))
    return render_template('dashboard/walkthrough/new_hours.jade', form=form)

@dashboard.route('/provider/menus/new', methods=['GET', 'POST'])
@login_required
def new_menus():
    provider = current_user.provider
    form = MenuItemForm()

    if not form.validate_on_submit():
        current_app.logger.info('bleah')
        if form.errors:
            flash(form.errors, 'error')
            current_app.logger.info(form.errors)

    else:
        menu_item = MenuItem(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data
        )

        got_it = False

        for menu in provider.menus:
            if menu.menu_type == request.form['menu_type']:
                menu.menu_items.append(menu_item)
            else:
                raise HSSError("Invalid Menu type")

        provider.save()
        provider.index()

    menus = provider.menus

    return render_template('dashboard/walkthrough/new_menus.jade',
            form=form, menus=menus)

@dashboard.route('/provider/general/new', methods=['GET', 'POST'])
@login_required
def new_general_info():
    provider = current_user.provider
    form = ProviderDashForm()
    current_app.logger.info(request.form)

    if form.validate_on_submit():
        if form.errors:
            flash(form.errors, 'error')
            current_app.logger.info(form.errors)

        else:
            provider.business_name      = form.business_name.data
            provider.phone              = form.phone.data
            provider.email              = form.email.data
            provider.payment_methods    = ' '.join(form.payment_methods.data)
            # fb url
            # twitter_url
            provider.save()


            return redirect(url_for('dashboard.new_hours'))
    return render_template('dashboard/walkthrough/new_general_info.jade', form=form)

@dashboard.route('/provider/address/new', methods=['GET', 'POST'])
@login_required
def new_address():
    provider = current_user.provider
    current_app.logger.info(provider.address)

    form = AddressForm(obj=provider.address)

    if form.validate_on_submit():
        if form.errors:
            flash(form.errors, 'error')
            current_app.logger.info(form.errors)

        else:
            provider.address.street_1   = form.street_1.data
            provider.address.street_2   = form.street_2.data
            provider.address.apartment  = form.apartment.data
            provider.address.city       = form.city.data
            provider.address.state      = form.state.data
            provider.address.zip_code   = form.zip_code.data
            provider.save()

            return redirect(url_for('dashboard.new_general_info'))

    return render_template('dashboard/walkthrough/new_address.jade', form=form)

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
