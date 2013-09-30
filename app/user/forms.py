from flask_wtf import Form
from wtforms import TextField, SubmitField
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


class PhotoForm(Form)
    image       = FileField(u'Upload Image')
    submit      = SubmitField(u'Submit')


class HoursForm(Form):
    monday          = TextField(u'Monday')
    tuesday         = TextField(u'Tuesday')
    wednesday       = TextField(u'Wednesday')
    thursday        = TextField(u'Thursday')
    friday          = TextField(u'Friday')
    saturday        = TextField(u'Saturday')
    sunday          = TextField(u'Sunday')


class AddressForm(Form):
    street_1        = TextField(u'Street 1')
    street_2        = TextField(u'Street 2')
    city            = TextField(u'City')
    state           = TextField(u'State')
    zip_code        = TextField(u'Zip Code')


class BusinessInfoForm(Form):
    business_name       = TextField(u'Business Name')
    payment_methods     = SelectMultipleField(u'Payment Methods',
                            choices=payment_methods)
    hours               = FormField(HoursForm, u'Hours')
    address             = FormField(AddressForm, u'Address')
    submit              = SubmitField(u'Submit')


class BioForm(Form):
    bio         = TextAreaField(u'About Me')
    fb          = TextField(u'Facebook url')
    twitter     = TextField(u'Twiiter url')
    links       = TextAreaField(u'Personal Links')
    submit      = SubmitField(u'Submit')


