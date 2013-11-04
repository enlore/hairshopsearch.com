from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField
from wtforms.validators import Required

menu_types = [('barber', 'barber'), ('salon', 'salon')]
class SearchForm(Form):
    menu_type       = SelectField('Type', choices=menu_types)
    service         = TextField('Service')
    zip_code        = TextField('Zip', [Required()])
    submit          = SubmitField('Search')
