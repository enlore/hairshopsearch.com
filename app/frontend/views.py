# -*- encoding: utf-8 -*-
from flask import Blueprint, render_template, current_app
from flask.ext.security import current_user, login_required
from sqlalchemy import or_
from ..user.models import Provider, Consumer

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

@frontend.route('/test_provider')
def test_provider():
    provider = Provider.query.first()
    return render_template('frontend/provider.html', provider=provider)

@frontend.route('/test_consumer')
def test_consumer():
    consumer = Consumer.query.first()
    return render_template('frontend/consumer.html', consumer=consumer)

@frontend.route('/welcome')
def welcome():
    return render_template('frontend/welcome.html')

@frontend.route('/new_provider', methods=['GET', 'POST'])
def new_provider():
    return 'new provider'

@frontend.route('/new_consumer', methods=['GET', 'POST'])
def new_consumer():
    return 'new consumer'

@frontend.route('/<provider_name>')
def provider(provider_name):
    """TODO"""
    return 'TODO'
