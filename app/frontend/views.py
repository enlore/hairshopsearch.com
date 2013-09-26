# -*- encoding: utf-8 -*-
from flask import Blueprint, render_template
from sqlalchemy import or_
from ..user.models import Provider

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def index():
    return 'index yo'

@frontend.route('/<provider_name>')
def provider(provider_name):
    provider = Provider.query.filter(or_(Provider.business_name==provider_name, Provider.id==provider_name))\
                .first()
    return render_template('frontend/provider.html', provider=provider)
