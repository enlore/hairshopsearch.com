from flask import Blueprint, render_template, redirect, url_for
from models import User
from forms import UserForm

user = Blueprint('user', 'user', template_folder='templates')

@user.route('/register')
def register():
    form = UserForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        app.logger.info(user.email + ' ' + user.password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.index'))
    return render_template('register.html')


