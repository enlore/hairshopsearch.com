from flask import Blueprint, render_template, redirect, url_for, current_app
from models import User
from forms import UserForm
from ..extensions import db

user = Blueprint('user', 'user', template_folder='templates')

@user.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()

    if form.validate_on_submit():
        current_app.logger.info('validated!')
        user = User()
        form.populate_obj(user)
        current_app.logger.info(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('frontend.index'))
    return render_template('user/register.html', form=form)


