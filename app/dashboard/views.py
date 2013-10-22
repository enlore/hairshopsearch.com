from flask import (Blueprint, render_template, current_app, redirect, url_for,
    flash)
from flask.ext.security import current_user, login_required
from sqlalchemy import or_
from ..user.models import (Provider, Consumer, Menu, MenuItem,
    ConsumerInstance, ProviderInstance)
from ..user.forms import (AddressForm, HoursForm, BioForm, PaymentsForm,
    MenuItemForm, RemoveItemForm, PhotoForm, SocialMediaForm,
    NewProviderForm, NewConsumerForm)
from ..core import db
from ..helpers import acceptable_url_string

dashboard = Blueprint('dashboard', __name__,
        url_prefix='/dashboard', template_folder='templates')

@dashboard.route('/')
def index():
    return 'd board'

@dashboard.route('/profile')
@login_required
def profile():
    rm_menu_item_form = RemoveItemForm()
    if current_user.consumer:
        return render_template('dashboard/consumer.html',
                consumer=current_user.consumer)

    if current_user.provider:
        return render_template('dashboard/provider.html',
                provider=current_user.provider,
                rm_menu_item_form=rm_menu_item_form)

    return redirect(url_for('frontend.welcome'))

@dashboard.route('/menu/<menu_id>/rm/<item_id>', methods=['GET'])
def rm_menu_item(menu_id, item_id):
    current_app.logger.info(str(menu_id) + ' ' + str(item_id))
    menu = Menu.query.filter(Menu.id==menu_id).first()
    menu_item = MenuItem.query.filter(MenuItem.id==item_id).first()

    current_app.logger.info(str(menu.id) + ' ' + str(menu_item.id))

    menu.menu_items.remove(menu_item)
    db.session.add(menu)
    db.session.commit()
    return redirect(url_for('dashboard.profile'))

@dashboard.route('/menu/add/<menu_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('dashboard.profile'))

    return render_template('dashboard/edit_profile.html', form=form,
            url=url_for('dashboard.add_menu_item', menu_id=menu_id))

@dashboard.route('/edit_nap', methods=['GET', 'POST'])
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
        return redirect(url_for('dashboard.profile'))

    else:
        flash(form.errors)

    return render_template('dashboard/edit_profile.html', form=form,
        url=url_for('dashboard.edit_nap'))

@dashboard.route('/edit_payment', methods=['GET', 'POST'])
@login_required
def edit_payment():
    form = PaymentsForm()
    if form.validate_on_submit():

        current_user.provider.payment_methods = \
            ','.join(form.payment_methods.data)

        db.session.add(current_user.provider)
        db.session.commit()

        return redirect(url_for('dashboard.profile'))

    return render_template('dashboard/edit_profile.html', form=form,
            url=url_for('dashboard.edit_payment'))

@dashboard.route('/edit_hours', methods=['GET', 'POST'])
@login_required
def edit_hours():
    form = HoursForm()

    if form.validate_on_submit():
        p = current_user.provider
        p.hours.monday_open     = form.monday_open.data
        p.hours.monday_close    = form.monday_close.data
        p.hours.tuesday_open    = form.tuesday_open.data
        p.hours.tuesday_close   = form.tuesday_close.data
        p.hours.wednesday_open  = form.wednesday_open.data
        p.hours.wednesday_close = form.wednesday_close.data
        p.hours.thursday_open   = form.thursday_open.data
        p.hours.thursday_close  = form.thursday_close.data
        p.hours.friday_open     = form.friday_open.data
        p.hours.friday_close    = form.friday_close.data
        p.hours.saturday_open   = form.saturday_open.data
        p.hours.saturday_close  = form.saturday_close.data
        p.hours.sunday_open     = form.sunday_open.data
        p.hours.sunday_close    = form.sunday_close.data

        db.session.add(current_user.provider)
        db.session.commit()
        return redirect(url_for('dashboard.profile'))

    return render_template('dashboard/edit_profile.html', form=form,
            url=url_for('dashboard.edit_hours'))

@dashboard.route('/edit_bio', methods=['GET', 'POST'])
@login_required
def edit_bio():
    form = BioForm()
    if form.validate_on_submit():
        current_user.provider.bio = form.bio.data

        db.session.add(current_user.provider)
        db.session.commit()

        return redirect(url_for('dashboard.profile'))

    return render_template('dashboard/edit_profile.html', form=form,
            url=url_for('dashboard.edit_bio'))

@dashboard.route('/edit_social_media', methods=['GET', 'POST'])
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

        return redirect(url_for('dashboard.profile'))

    return render_template('dashboard/edit_profile.html', form=form,
            url=url_for('dashboard.edit_social_media'))

@dashboard.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    form = PhotoForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard.profile'))
    return render_template('dashboard/edit_profile.html', form=form,
            url=url_for('dashboard.upload_photo'))

@dashboard.route('/new_provider', methods=['GET', 'POST'])
@login_required
def new_provider():
    form = NewProviderForm()
    if form.validate_on_submit():
        provider = Provider(user=current_user)

        provider.business_name = form.business_name.data
        provider.payment_methods = ''

        dirty_name = provider.business_name
        clean_name = acceptable_url_string(dirty_name,
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

        db.session.add(pi)
        db.session.add(provider)
        db.session.commit()
        return redirect(url_for('dashboard.profile'))
    return render_template('dashboard/new_provider.html', form=form)

@dashboard.route('/new_consumer', methods=['GET', 'POST'])
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
        clean_name = acceptable_url_string(dirty_name,
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
