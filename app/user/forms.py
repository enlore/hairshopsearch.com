from flask_wtf import Form
from wtforms import (TextField, TextAreaField, FileField, SelectMultipleField,
        SelectField, FormField, SubmitField)
from wtforms.validators import Required


# CONSUMER
# a Hair Log Form
# a Bio form (Links, social media, bio)
# A photo form

# PROVIDER
# a Menu Form
# A photo form
# a Business Info form (NAP, Payments)
# a Review Form

class ReviewForm(Form):
    body        = TextAreaField('')
    author      = TextField('')
    submit      = SubmitField(u'Submit')


class PhotoForm(Form):
    image       = FileField(u'Upload Image')
    submit      = SubmitField(u'Submit')

times = [('5:00am', '5:00am'), ('5:15am', '5:15am'), ('5:30am', '5:30am'),
        ('5:45am', '5:45am'), ('6:00am', '6:00am'), ('6:15am', '6:15am'),
        ('6:30am', '6:30am'), ('6:45am', '6:45am'), ('7:00am', '7:00am'),
        ('7:15am', '7:15am'), ('7:30am', '7:30am'), ('7:45am', '7:45am'),
        ('8:00am', '8:00am'), ('8:15am', '8:15am'), ('8:30am', '8:30am'),
        ('8:45am', '8:45am'), ('9:00am', '9:00am'), ('9:15am', '9:15am'),
        ('9:30am', '9:30am'), ('9:45am', '9:45am'), ('10:00am', '10:00am'),
        ('10:15am', '10:15am'), ('10:30am', '10:30am'), ('10:45am', '10:45am'),
        ('11:00am', '11:00am'), ('11:15am', '11:15am'), ('11:30am', '11:30am'),
        ('11:45am', '11:45am'), ('12:00pm', '12:00pm'), ('12:15pm', '12:15pm'),
        ('12:30pm', '12:30pm'), ('12:45pm', '12:45pm'), ('1:00pm', '1:00pm'),
        ('1:15pm', '1:15pm'), ('1:30pm', '1:30pm'), ('1:45pm', '1:45pm'),
        ('2:00pm', '2:00pm'), ('2:15pm', '2:15pm'), ('2:30pm', '2:30pm'),
        ('2:45pm', '2:45pm'), ('3:00pm', '3:00pm'), ('3:15pm', '3:15pm'),
        ('3:30pm', '3:30pm'), ('3:45pm', '3:45pm'), ('4:00pm', '4:00pm'),
        ('4:15pm', '4:15pm'), ('4:30pm', '4:30pm'), ('4:45pm', '4:45pm'),
        ('5:00pm', '5:00pm'), ('5:15pm', '5:15pm'), ('5:30pm', '5:30pm'),
        ('5:45pm', '5:45pm'), ('6:00pm', '6:00pm'), ('6:15pm', '6:15pm'),
        ('6:30pm', '6:30pm'), ('6:45pm', '6:45pm'), ('7:00pm', '7:00pm'),
        ('7:15pm', '7:15pm'), ('7:30pm', '7:30pm'), ('7:45pm', '7:45pm'),
        ('8:00pm', '8:00pm'), ('8:15pm', '8:15pm'), ('8:30pm', '8:30pm'),
        ('8:45pm', '8:45pm'), ('9:00pm', '9:00pm'), ('9:15pm', '9:15pm'),
        ('9:30pm', '9:30pm'), ('9:45pm', '9:45pm'), ('10:00pm', '10:00pm'),
        ('10:15pm', '10:15pm'), ('10:30pm', '10:30pm'), ('10:45pm', '10:45pm'),
        ('11:00pm', '11:00pm'), ('11:15pm', '11:15pm'), ('11:30pm', '11:30pm'),
        ('11:45pm', '11:45pm'), ('12:00am', '12:00am')]

class HoursForm(Form):
    monday          = SelectField(u'Monday', choices=times)
    tuesday         = SelectField(u'Tuesday',choices=times)
    wednesday       = SelectField(u'Wednesday', choices=times)
    thursday        = SelectField(u'Thursday', choices=times)
    friday          = SelectField(u'Friday', choices=times)
    saturday        = SelectField(u'Saturday', choices=times)
    sunday          = SelectField(u'Sunday', choices=times)
    submit          = SubmitField(u'Submit')


class AddressForm(Form):
    business_name   = TextField(u'Business Name')
    phone           = TextField(u'Phone')
    street_1        = TextField(u'Street 1')
    street_2        = TextField(u'Street 2')
    city            = TextField(u'City')
    state           = TextField(u'State')
    zip_code        = TextField(u'Zip Code')
    submit          = SubmitField(u'Submit')


payment_methods = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('amex', 'Amex')
        ]

class PaymentsForm(Form):
    payment_methods     = SelectMultipleField(u'Payment Methods',
                            choices=payment_methods)
    submit              = SubmitField(u'Submit')


class BioForm(Form):
    bio         = TextAreaField(u'About Me')
    submit      = SubmitField(u'Submit')

class SocialMediaForm(Form):
    fb          = TextField(u'Facebook url')
    twitter     = TextField(u'Twiiter url')
    link       = TextAreaField(u'Personal Website')
    submit      = SubmitField(u'Submit')

class MenuForm(Form):
    pass
