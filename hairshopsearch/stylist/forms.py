from flask_wtf import Form
from wtforms import TextField, SubmitField
from wtforms.validators import Required
from ..user import UserForm

class StylistForm(UserForm):
    avatar          = TextField(u'Avatar:')
    blurb           = TextField(u'About You:')
    salon           = TextField(u'Salon:')
    submit          = SubmitField(u'Sign Up!')
