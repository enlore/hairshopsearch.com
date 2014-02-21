from flask_wtf import Form
from wtforms import TextField, SubmitField

class ConsumerInfoForm(Form):
    first_name      = TextField('First Name')
    last_name       = TextField('Last Name')
    email           = TextField('Email')
    submit          = SubmitField('Save Changes')
