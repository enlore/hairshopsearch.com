# -*- encoding: utf-8 -*-
from flask import (Blueprint, render_template, current_app, redirect, url_for,
    flash)
from flask.ext.security import login_required
from ..user.models import Provider, Consumer

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def index():
    return render_template('frontend/index.html')

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

