from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField

class TestForm(Form):
    name        = TextField()
    last        = TextField()
    submit      = SubmitField()
