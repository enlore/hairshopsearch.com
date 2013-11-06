from flask import (Blueprint, render_template, current_app, redirect, url_for,
    flash, request, jsonify)
from flask.ext.security import current_user, login_required
from sqlalchemy import or_
from ..user.forms import (AddressForm, HoursForm, BioForm, PaymentsForm,
    MenuItemForm, RemoveItemForm, PhotoForm, SocialMediaForm,
    NewProviderForm, NewConsumerForm, HairInfoForm, ProductForm,
    RoutineForm)
from ..models import (Provider, Consumer, Menu, MenuItem,
    ConsumerInstance, ProviderInstance, Address, Hours, Photo, Product)
from ..core import db
from ..helpers import acceptable_url_string

dashboard = Blueprint('dashboard', __name__,
        url_prefix='/dashboard', template_folder='templates')


@dashboard.route('/photo/save', methods=['POST'])
def save_photo():
    entity = current_user.provider or current_user.consumer
    current_app.logger.info(entity)

    if not entity.avatar:
        entity.avatar = Photo()

    photo_url = '{}/{}'.format(
            current_app.config['S3_URL'],
            request.form['photo_key']
            )

    current_app.logger.info(photo_url)
    entity.avatar.url = photo_url
    db.session.add(entity)

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e.msg)
        return jsonify(status='Your file wasn\'t saved! Please try again.')

    return redirect(url_for('dashboard.profile'))


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

@dashboard.route('/consumer/bio/edit', methods=['GET', 'POST'])
def edit_consumer_bio():
    c = current_user.consumer
    form = BioForm(obj=c)
    if form.validate_on_submit():
        current_app.logger.info(form.bio.data)
        c.bio = form.bio.data
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('dashboard.profile'))
    return render_template('dashboard/edit_profile.html', form=form,
            url=url_for('dashboard.edit_consumer_bio'))

@dashboard.route('/consumer/hair_type/edit', methods=['GET', 'POST'])
def edit_consumer_hair_type():
    c = current_user.consumer
    form = HairInfoForm(obj=c)
    if form.validate_on_submit():
        c.hair_type = form.hair_type.data
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('dashboard.profile'))
    return render_template('dashboard/edit_profile.html', form=form,
            url=url_for('dashboard.edit_consumer_hair_type'))

@dashboard.route('/consumer/products/add', methods=['GET', 'POST'])
def add_product():
    c = current_user.consumer
    form = ProductForm()
    if form.validate_on_submit():
        product = Product()
        product.name = form.name.data
        product.description = form.description.data

        c.hair_products.append(product)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('dashboard.profile'))

    return render_template('dashboard/edit_profile.html', form=form,
            url=url_for('dashboard.add_product'))

@dashboard.route('/consumer/routine/edit', methods=['GET', 'POST'])
def edit_routine():
    c = current_user.consumer
    form = RoutineForm(obj=c)
    if form.validate_on_submit():
        c.hair_routine = form.routine.data
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('dashboard.profile'))
    return render_template('dashboard/edit_profile.html', form=form,
            url=url_for('dashboard.edit_routine'))

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
    if not p.address:
        p.address = Address()

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
    p = current_user.provider
    form = HoursForm()
    if not p.hours:
        p.hours = Hours()

    if form.validate_on_submit():
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

    form.monday_open.data       = p.hours.monday_open
    form.monday_close.data      = p.hours.monday_open
    form.tuesday_open.data      = p.hours.monday_close
    form.tuesday_close.data     = p.hours.tuesday_open
    form.wednesday_open.data    = p.hours.tuesday_close
    form.wednesday_close.data   = p.hours.wednesday_open
    form.thursday_open.data     = p.hours.wednesday_close
    form.thursday_close.data    = p.hours.thursday_open
    form.friday_open.data       = p.hours.thursday_close
    form.friday_close.data      = p.hours.friday_open
    form.saturday_open.data     = p.hours.friday_close
    form.saturday_close.data    = p.hours.saturday_open
    form.sunday_open.data       = p.hours.saturday_close
    form.sunday_close.data      = p.hours.sunday_open

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

@dashboard.route('/new_provider', methods=['GET', 'POST'])
@login_required
def new_provider():
    form = NewProviderForm()
    if form.validate_on_submit():
        provider = Provider(user=current_user)

        provider.business_name = form.business_name.data
        provider.payment_methods = ''

        for _type in ['barbershop', 'salon', 'product']:
            menu = Menu(menu_type=_type)
            provider.menus.append(menu)

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
