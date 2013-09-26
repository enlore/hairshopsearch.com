# -*- encoding: utf-8 -*-
from flask import Blueprint, render_template
from sqlalchemy import or_
from ..user.models import Provider, Consumer

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def index():
    return 'index yo'

@frontend.route('/<provider_name>')
def provider(provider_name):
    provider = Provider.query.filter(or_(Provider.business_name==provider_name, Provider.id==provider_name))\
                .first()
    return render_template('frontend/provider.html', provider=provider)

@frontend.route('/consumer/<consumer_id>')
def consumer(consumer_id):
    consumer = Consumer.query.filter(Consumer.id==consumer_id).first()
    return render_template('frontend/consumer.html', consumer=consumer)
