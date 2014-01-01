# -*- encoding: utf-8 -*-
from flask import (Blueprint, render_template, current_app, redirect, url_for,
    flash, abort)
from flask.ext.security import login_required, roles_required, current_user

from ..search.forms import SearchForm

from ..provider.models import Provider
from ..consumer.models import Consumer
from ..models import User

from ..config import Config
from ..core import db

if Config.DEV:
    from ..forms import TestForm

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/<user_id>/gallery')
def gallery(user_id):
    title = 'Gallery'
    user = User.query.get(user_id)
    entity = user.provider or user.consumer
    gallery = entity.gallery
    return render_template('frontend/gallery.html', title=title, gallery=gallery)


@frontend.route('/test_flash')
def test_flash():
    flash('An error, oh noes!', 'error')
    flash('Some helpful info.', 'info')
    flash('To drive your enemies before you', 'success')
    return redirect(url_for('frontend.index'))

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
#@login_required
def welcome():
    return render_template('frontend/welcome.html')


@login_required
@roles_required(['consumer'])
@frontend.route('/<int:consumer_id>/follow')
def follow(consumer_id):
    first_person = current_user.consumer
    consumer = Consumer.query.get(consumer_id)

    first_person.follows.append(consumer)
    db.session.add(first_person)
    db.session.commit()

    return redirect(url_for('frontend.consumer_url',
        consumer_url=consumer.consumer_url))

@frontend.route('/provider_welcome')
def provider_welcome():
    return render_template('frontend/provider_marketing.html')

@frontend.route('/consumer_welcome')
def consumer_welcome():
    return render_template('frontend/consumer_marketing.html')

@frontend.route('/tos')
def tos():
    return render_template('frontend/tos.html')

@frontend.route('/privacy_policy')
def privacy_policy():
    return render_template('frontend/privacy_policy.html')

if Config.DEV == True:
    @frontend.route('/sandbox')
    def sandbox():
        form = TestForm()
        return render_template('frontend/sandbox.html', form=form)
