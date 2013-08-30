from flask import Blueprint, render_template, redirect, url_for, current_app
from ..user import User
from models import SalonManager
from forms import SalonManagerForm
from ..extensions import db
from ..util import SALON_MANAGER

salonmanager = Blueprint('salonmanager', 'salonmanager',
        template_folder='salonmanager/templates', url_prefix='/salon')

@salonmanager.route('/')
def index():
    current_app.logger.info(salonmanager.template_folder)
    return 'salon manager index'

@salonmanager.route('/register', methods=['GET', 'POST'])
def register():
    form = SalonManagerForm()
    if form.validate_on_submit():
        sm = SalonManager()
        form.populate_obj(sm)
        sm.user = User()
        sm.user.email = form.email.data
        sm.user.first_name = form.first_name.data
        sm.user.last_name = form.last_name.data
        sm.user.password = form.password.data
        sm.user.role = SALON_MANAGER
        db.session.add(sm)
        db.session.commit()
        return redirect(url_for('frontend.index'))
    return render_template('salonmanager/register.html', form=form)
