# -*- encoding: utf-8 -*-
from flask import (Blueprint, render_template, current_app, redirect, url_for,
    flash)
from flask.ext.security import current_user, login_required
from sqlalchemy import or_
from ..user.models import Provider, Consumer
from ..user.forms import (AddressForm, HoursForm, BioForm, PaymentsForm,
    SocialMediaForm, )
from ..core import db

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def index():
    return render_template('frontend/index.html')

@frontend.route('/edit_menu', methods=['GET', 'POST'])
@frontend.route('/edit_menu/<menu_type>', methods=['GET', 'POST'])
@login_required
def edit_menu(menu_type):
    return 'edit %s' % menu_type

@frontend.route('/profile')
@login_required
def profile():
    if current_user.consumer:
        return render_template('frontend/consumer.html',
                consumer=current_user.consumer)

    if current_user.provider:
        return render_template('frontend/provider.html',
                provider=current_user.provider)

@frontend.route('/edit_nap', methods=['GET', 'POST'])
@login_required
def edit_nap():
    form = AddressForm(obj=current_user.provider.address)
    p = current_user.provider
    form.business_name.data  = p.business_name
    form.phone.data          = p.phone 

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
        current_app.logger.info('flashing')
        flash(form.errors)

    return render_template('frontend/edit_profile.html', form=form,
        url=url_for('frontend.edit_nap'))

@frontend.route('/edit_payment', methods=['GET', 'POST'])
def edit_payment():
    form = PaymentsForm()
    return render_template('frontend/edit_profile.html', form=form,
            url=url_for('frontend.edit_payment'))

@frontend.route('/edit_hours', methods=['GET', 'POST'])
def edit_hours():
    form = HoursForm()
    return render_template('frontend/edit_profile.html', form=form,
            url=url_for('frontend.edit_hours'))

@frontend.route('/edit_bio', methods=['GET', 'POST'])
def edit_bio():
    form = BioForm()
    return render_template('frontend/edit_profile.html', form=form,
            url=url_for('frontend.edit_bio'))

@frontend.route('/edit_social_media', methods=['GET', 'POST'])
def edit_social_media():
    form = SocialMediaForm()
    return render_template('frontend/edit_profile.html', form=form,
            url=url_for('frontend.edit_social_media'))

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
