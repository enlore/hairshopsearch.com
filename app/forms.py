from flask_wtf import Form
from wtforms import TextField, TextAreaField, FileField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import Required

from markupsafe import Markup

class TestForm(Form):
    name        = TextField()
    last        = TextField()
    submit      = SubmitField()


hair_condition = [
    ('exceptionally_curly', 'Exceptionally Curly (4a, 4b, 4c)'),
    ('curly', 'Curly (3a, 3b, 3c)'),
    ('wavy', 'Wavy (2a, 2b, 2c)'),
    ('straight', 'Straight (1a, 1b, 1c)')
        ]

scalp_condition = [
    ('oily', 'Oily'),
    ('dry', 'Dry'),
    ('flaky', 'Flaky'),
    ('itchy', 'Itchy'),
    ('normal', 'Normal')
        ]

trim_last = treat_last = [
    ('', '0 - 4 weeks ago'),
    ('', '1 - 3 months ago'),
    ('', '3 - 6 months ago'),
    ('', '6 - 12 months ago'),
    ('', '1 year or month')
        ]

maintenance_freq = [
    ('', 'Daily'),
    ('', 'Twice a week'),
    ('', 'Once a week'),
    ('', 'Twice a month'),
    ('', 'Once a month'),
    ('', 'Every other month')
        ]

class ConsumerDashForm(Form):
    avatar          = FileField('Profile Photo')
    first_name      = TextField('First Name', [Required()])
    last_name       = TextField('Last Name', [Required()])
    email           = TextField('Email', [Required()])
    gender          = SelectField('Gender', choices=[
                        ('male', 'Male'),
                        ('female', 'Female'),
                        ('rather_not', 'Rather Not Say')
                    ])
    birth_day       = TextField('Birthday')
    location        = TextField('Ciy, State')

    hair_condition  = SelectField('What is your hair condition?',
                        choices=hair_condition)

    scalp_condition = SelectField('What is your scalp condition?',
                        choices=scalp_condition)

    treat           = SelectField('Do you chemically treat your hair?',
                        coerce=int,
                        choices=[(1, 'Yes'), (0, 'No')])

    last_treat      = SelectField('When was your last treatment?',
                        choices=treat_last)

    fav_style       = TextField('What is your favorite cut or style?')

    shampoo         = TextField('What shampoo do you use?')
    shampoo_freq    = SelectField('How often do you shampoo your hair?',
                        choices=maintenance_freq)

    conditioner     = TextField('What conditioner do you use?')
    condition_freq  = SelectField('How often do you condition your hair?',
                        choices=maintenance_freq)

    trim_last       = SelectField('When was your hair last trimmed?',
                        choices=trim_last)

    facebook_url    = TextField('Link your Facebook Page')
    google_plus_url = TextField('Link your G+ page')
    blog_url        = TextField('Link your blog')
    youtube_url     = TextField('Link your youtube account')
    submit          = SubmitField('Save Changes')


payment_methods = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('amex', 'Amex')
        ]


def multi_checkboxes(field, ul_class=u'', **kwargs):
    html = []
    html.append(Markup('<ul>'))
    for value, label, checked in field.iter_choices():
        html.append(Markup('<li>'))

        if checked:
            html.append(Markup('<input id ="{}-{}" type="checkbox" name="{}" \
                    value="{}" checked="checked">{}</input>'.format(
                        field.id,
                        value,
                        field.name,
                        value,
                        label)))
        else:
            html.append(Markup('<input id ="{}-{}" type="checkbox" name="{}" \
                    value="{}">{}</input>'.format(
                        field.id,
                        value,
                        field.name,
                        value,
                        label)))


        html.append(Markup('</li>'))
    html.append(Markup('</ul>'))
    return Markup('\n').join(html)


class ProviderDashForm(Form):
    avatar          = TextField('Avatar')
    business_name   = TextField('Business Name')
    phone           = TextField('Phone Number')
    email           = TextField('Business Email')

    street_1        = TextField('Street')
    street_2        = TextField('Street 2')
    city            = TextField('City')
    state           = TextField('State')
    zip_code        = TextField('Zip')

    payment_methods     = SelectMultipleField(u'Payment Methods',
                            widget=multi_checkboxes,
                            choices=payment_methods)

    bio             = TextField('About Us')
    fb_url          = TextField('Facebook Page')
    twitter_url     = TextField('Twitter')

    submit          = SubmitField('Save Changes')
