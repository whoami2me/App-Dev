from wtforms import Form, StringField, TextAreaField, validators, IntegerField, RadioField, SelectField
from flask_wtf.file import FileField
from wtforms.fields import DateField


class CreateEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    location = StringField('Location', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateOEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    event_status = SelectField('Event Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed'), ('O', 'Open-In-Advance')], default='O')
    reg_status = SelectField('Registration Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed')], default='O')


class CreateOfflineEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    pax = IntegerField('Pax', [validators.NumberRange(min=0, max=200), validators.DataRequired()])
    location = StringField('Location', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateOffEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    pax = IntegerField('Pax', [validators.NumberRange(min=0, max=200), validators.DataRequired()])
    location = StringField('Location', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_status = SelectField('Event Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed'), ('O', 'Open-In-Advance')], default='O')
    reg_status = SelectField('Registration Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed')], default='O')

