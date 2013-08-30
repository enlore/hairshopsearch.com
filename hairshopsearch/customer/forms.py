from flask_wtf import Form
from wtforms import SubmitField
from ..user.forms import UserForm

class CustomerForm(UserForm):
    submit          = SubmitField(u'Sign up!')
