# -*- encoding: utf-8 -*-
from flask import (Blueprint, render_template, current_app, redirect, url_for,
    flash)
from flask.ext.security import current_user, login_required
from sqlalchemy import or_
from ..user.models import Provider, Consumer
from ..user.forms import AddressForm
from ..core import db

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def index():
    return render_template('frontend/index.html')

@frontend.route('/profile')
@login_required
def profile():
    if current_user.consumer:
        return render_template('frontend/consumer.html',
                consumer=current_user.consumer)

    if current_user.provider:
        return render_template('frontend/provider.html',
                provider=current_user.provider)

    return render_template('frontend/provider.html', provider=current_user.provider)

@frontend.route('/edit_nap', methods=['GET', 'POST'])
@login_required
def edit_nap():
    form = AddressForm()
    if form.validate_on_submit():
        return redirect(url_for('frontend.profile'))
    else:
        flash(form.errors)
    return render_template('frontend/edit_profile.html', form=form)

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
