from flask_wtf import Form
from wtforms import (TextField, PasswordField, SubmitField, ValidationError)
from wtforms.validators import Required, Email


class UserForm(Form):
    email               = TextField(u'Email:', [Required(), Email()])
    first_name          = TextField(u'First Name:', [Required()])
    last_name           = TextField(u'Last Name:')
    password            = PasswordField(u'Password:', [Required()])
    confirm_password    = PasswordField(u'Confirm Password:', [Required()])

    def validate_password(form, password):
        if not password.data == form.confirm_password.data:
            raise ValidationError('Passwords do not match')
