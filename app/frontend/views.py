# -*- encoding: utf-8 -*-
from flask import (Blueprint, render_template, current_app, redirect, url_for,
    flash, abort)
from flask.ext.security import login_required, roles_required, current_user
from ..search.forms import SearchForm
from ..models import Provider, Consumer, User
from ..core import db

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def index():
    return render_template('frontend/index.html',
            index_search_form=SearchForm())

@login_required
@frontend.route('/<provider_id>/favorite')
def favorite(provider_id):
    this_provider = Provider.query.get(provider_id)

    if not this_provider.business_url:
        this_provider.business_url = this_provider.business_name

    if current_user.is_anonymous():
        current_app.logger.info('anon anon')
        abort(403)

    if this_provider not in current_user.consumer.favorites:
        current_user.consumer.favorites.append(this_provider)

    db.session.add(current_user)
    db.session.commit()

    return redirect(url_for('frontend.provider_url',
        provider_url=this_provider.business_url))

@frontend.route('/<provider_url>')
def provider_url(provider_url):
    p = Provider.query.filter(Provider._business_url==provider_url.lower()).first()
    if p:
        return render_template('frontend/provider.html', provider=p)
    else:
        abort(404)

@frontend.route('/consumer/<consumer_url>')
def consumer_url(consumer_url):
    c = Consumer.query.filter(Consumer.consumer_url==consumer_url.lower()).first()
    current_app.logger.info(c)
    if c:
        return render_template('frontend/consumer.html', consumer=c)
    else:
        abort(404)

@login_required
@frontend.route('/<int:provider_id>/endorse')
def endorse(provider_id):
    if not current_user.provider:
        return abort()
    endorsee = Provider.query.filter(Provider.id == provider_id).first()
    current_user.provider.endorses.append(endorsee)
    db.session.add(current_user.provider)
    db.session.commit()
    return redirect(url_for('frontend.provider_url',
        provider_url=endorsee.business_url))

@frontend.route('/test_provider')
def test_provider():
    provider = Provider.query.first()
    current_app.logger.info(provider.business_url)
    if not provider.business_url:
        provider.business_url = provider.business_name
    return render_template('frontend/provider.html', provider=provider)

@frontend.route('/test_consumer')
def test_consumer():
    consumer = Consumer.query.first()
    return render_template('frontend/consumer.html', consumer=consumer)

@frontend.route('/welcome')
@login_required
def welcome():
    return render_template('frontend/welcome.html')

