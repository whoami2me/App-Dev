from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, IntegerField
from flask_wtf.file import FileField
from wtforms.fields import  DateField

class CreateEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    location = StringField('Location', [validators.Length(min=1, max=150), validators.DataRequired()])

class CreateOfflineEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    pax = IntegerField('Pax', [validators.NumberRange(min=0, max=200), validators.DataRequired()])
    location = StringField('Location', [validators.Length(min=1, max=150), validators.DataRequired()])
