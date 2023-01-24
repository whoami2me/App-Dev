from wtforms import Form, StringField, TextAreaField, validators, IntegerField, SelectField
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms.fields import DateField
from wtforms_validators import AlphaNumeric


class CreateEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    description = TextAreaField('Description', [validators.Length(min=1, max=150), validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    location = SelectField('Location', validators=[validators.DataRequired()], choices=[('Z', 'Zoom'), ('G', 'Google Meets'), ('C', 'Cisco Webex')], default='')


class CreateOEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg' ,'gif'])])
    description = TextAreaField('Description', [validators.Length(min=1, max=150), validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    location = SelectField('Location', validators=[validators.DataRequired()], choices=[('Z', 'Zoom'), ('G', 'Google Meets'), ('C', 'Cisco Webex')], default='')
    event_status = SelectField('Event Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed'), ('O', 'Open-In-Advance')], default='O')
    reg_status = SelectField('Registration Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed')], default='O')


class CreateOfflineEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg' ,'gif'])])
    description = TextAreaField('Description', [validators.Length(min=1, max=150), validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    pax = IntegerField('Pax', [validators.NumberRange(min=0, max=1000), validators.DataRequired()])
    location = StringField('Location', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateOffEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg' ,'gif'])])
    description = TextAreaField('Description', [validators.Length(min=1, max=150), validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    pax = IntegerField('Pax', [validators.NumberRange(min=0, max=1000), validators.DataRequired()])
    location = StringField('Location', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_status = SelectField('Event Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed'), ('O', 'Open-In-Advance')], default='O')
    reg_status = SelectField('Registration Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed')], default='O')

