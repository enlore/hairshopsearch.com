from flask_wtf import Form
from wtforms import TextField, SubmitField

class SearchForm(Form):
    business_name   = TextField('')
    submit          = SubmitField('Search')
