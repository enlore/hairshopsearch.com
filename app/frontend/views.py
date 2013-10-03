# -*- encoding: utf-8 -*-
from flask import (Blueprint, render_template, current_app, redirect, url_for,
    flash)
from flask.ext.security import current_user, login_required
from sqlalchemy import or_
from ..user.models import Provider, Consumer, Menu, MenuItem
from ..user.forms import (AddressForm, HoursForm, BioForm, PaymentsForm,
    MenuItemForm, RemoveItemForm, PhotoForm, SocialMediaForm, )
from ..core import db

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def index():
    return render_template('frontend/index.html')


@frontend.route('/profile')
@login_required
def profile():
    rm_menu_item_form = RemoveItemForm()
    if current_user.consumer:
        return render_template('frontend/consumer.html',
                consumer=current_user.consumer)

    if current_user.provider:
        return render_template('frontend/provider.html',
                provider=current_user.provider,
                rm_menu_item_form=rm_menu_item_form)

@frontend.route('/menu/<menu_id>/rm/<item_id>', methods=['POST'])
def rm_menu_item(item_id, menu_id):
    menu = Menu.query.filter(Menu.id==menu_id).first()
    menu_item = MenuItem.query.filter(MenuItem.id==item_id).first()
    menu.menu_items.remove(menu_item)
    db.session.add(menu)
    db.session.commit()
    return redirect(url_for('frontend.profile'))

@frontend.route('/menu/add/<menu_id>', methods=['GET', 'POST'])
def add_menu_item(menu_id):
    form = MenuItemForm()
    menu = Menu.query.filter(Menu.id==menu_id).first()
    if form.validate_on_submit():
        menu.menu_items.append(MenuItem(
            name=form.name.data,
            price=form.price.data))
        current_user.provider.menus.append(menu)
        db.session.add(current_user.provider)
        db.session.commit()
        return redirect(url_for('frontend.profile'))

    return render_template('frontend/edit_profile.html', form=form,
            url=url_for('frontend.add_menu_item', menu_id=menu_id))

@frontend.route('/edit_nap', methods=['GET', 'POST'])
@login_required
def edit_nap():
    p = current_user.provider
    form = AddressForm(
            obj=current_user.provider.address,
            business_name=p.business_name,
            phone=p.phone)

    if form.validate_on_submit():
        p.address.street_1  = form.street_1.data
        p.address.street_2  = form.street_2.data
        p.address.city      = form.city.data
        p.address.state     = form.state.data
        p.address.zip_code  = form.zip_code.data

        p.business_name     = form.business_name.data
        p.phone             = form.phone.data

        db.session.add(current_user.provider.address)
        db.session.commit()
        flash('Update successful!', 'success')
        return redirect(url_for('frontend.profile'))

    else:
        flash(form.errors)

    return render_template('frontend/edit_profile.html', form=form,
        url=url_for('frontend.edit_nap'))

@frontend.route('/edit_payment', methods=['GET', 'POST'])
@login_required
def edit_payment():
    form = PaymentsForm()
    if form.validate_on_submit():

        current_user.provider.payment_methods = \
            ','.join(form.payment_methods.data)

        db.session.add(current_user.provider)
        db.session.commit()

        return redirect(url_for('frontend.profile'))

    return render_template('frontend/edit_profile.html', form=form,
            url=url_for('frontend.edit_payment'))

@frontend.route('/edit_hours', methods=['GET', 'POST'])
@login_required
def edit_hours():
    form = HoursForm()
    if form.validate_on_submit():
        return redirect(url_for('frontend.profile'))
    return render_template('frontend/edit_profile.html', form=form,
            url=url_for('frontend.edit_hours'))

@frontend.route('/edit_bio', methods=['GET', 'POST'])
@login_required
def edit_bio():
    form = BioForm()
    if form.validate_on_submit():
        current_user.provider.bio = form.bio.data

        db.session.add(current_user.provider)
        db.session.commit()

        return redirect(url_for('frontend.profile'))

    return render_template('frontend/edit_profile.html', form=form,
            url=url_for('frontend.edit_bio'))

@frontend.route('/edit_social_media', methods=['GET', 'POST'])
@login_required
def edit_social_media():
    form = SocialMediaForm(obj=current_user.provider)

    if form.validate_on_submit():
        current_user.provider.fb_url        = form.fb_url.data
        current_user.provider.twitter_url   = form.twitter_url.data
        current_user.provider.links         = form.link.data

        db.session.add(current_user.provider)
        db.session.commit()
        current_app.logger.info(current_user.provider.fb_url)

        return redirect(url_for('frontend.profile'))

    return render_template('frontend/edit_profile.html', form=form,
            url=url_for('frontend.edit_social_media'))

@frontend.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    form = PhotoForm()
    if form.validate_on_submit():
        return redirect(url_for('frontend.profile'))
    return render_template('frontend/edit_profile.html', form=form,
            url=url_for('frontend.upload_photo'))

@frontend.route('/test_provider')
def test_provider():
    provider = Provider.query.first()
    return render_template('frontend/provider.html', provider=provider)

@frontend.route('/test_consumer')
def test_consumer():
    consumer = Consumer.query.first()
    return render_template('frontend/consumer.html', consumer=consumer)

@frontend.route('/welcome')
@login_required
def welcome():
    return render_template('frontend/welcome.html')

@frontend.route('/new_provider', methods=['GET', 'POST'])
@login_required
def new_provider():
    provider = Provider(user=current_user)
    current_user.provider = provider
    provider.payment_methods = ''
    provider.hours = {}
    db.session.add(current_user.provider)
    db.session.commit()
    return redirect(url_for('frontend.profile'))

@frontend.route('/new_consumer', methods=['GET', 'POST'])
@login_required
def new_consumer():
    current_user.consumer = Consumer(user=current_user)
    db.session.add(current_user.consumer)
    db.session.commit()
    return redirect(url_for('frontend.profile'))

@frontend.route('/<provider_name>')
def provider(provider_name):
    """TODO"""
    return 'TODO'
