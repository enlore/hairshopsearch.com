from flask import Blueprint, render_template, redirect, url_for
from .forms import StylistForm
from .models import Stylist
from ..user import User
from ..extensions import db
from ..salonmanager.models import SalonManager

stylist = Blueprint('stylist', 'stylist', url_prefix='/stylist')

@stylist.route('/')
def index():
    return 'stylist index'

@stylist.route('/register', methods=['GET', 'POST'])
def register():
    form = StylistForm()
    if form.validate_on_submit():
        stylist = Stylist()
        stylist.avatar = form.avatar.data
        stylist.blurb = form.blurb.data


        salon = SalonManager.query.filter_by(
                business_name=form.salon.data.lower()).first()
        stylist.salon = salon

        stylist.user = User()
        form.populate_obj(stylist.user)

        db.session.add(stylist)
        db.session.commit()
        return redirect(url_for('frontend.index'))
    return render_template('stylist/register.html', form=form)
