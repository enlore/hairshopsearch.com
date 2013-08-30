from ..user import UserForm
from wtforms import TextField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Required, Email

class SalonManagerForm(UserForm):
    business_name           = TextField(u'Business Name:', [Required()])
    hours                   = TextField(u'Hours of Operation:')
    phone                   = TextField(u'Phone:', [Required()])
    street_address          = TextField(u'Street:', [Required()])
    city                    = TextField(u'City:', [Required()])
    state                   = TextField(u'State', [Required()])
    zip_code                = TextField(u'Zip', [Required()])
    avatar                  = TextField(u'Personal Avatar')
    submit                  = SubmitField(u'Sign Up!')
