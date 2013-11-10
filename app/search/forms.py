from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField
from wtforms.validators import Required

menu_types = [
        ('none', 'I\'m looking for:'),
        ('salon', 'Salons'),
        ('barber', 'Barbershops'),
        ('product', 'Products')]

class SearchForm(Form):
    menu_type       = SelectField('Type', choices=menu_types)
    service         = TextField('Service', default="services")
    zip_code        = TextField('Zip', [Required()], default='zip code')
    submit          = SubmitField('Search')
