from datetime import date
from wtforms import Form, StringField, TextAreaField, validators, IntegerField, SelectField, ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import DateField



class CreateEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150,message="It should be in a range from 1 to 150!"), validators.DataRequired(), validators.Regexp('[a-zA-Z0-9_-]+$', message="It should only contain letters, numbers , underscores and dashes")])
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    description = TextAreaField('Description', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    location = SelectField('Location', validators=[validators.DataRequired()], choices=[('Z', 'Zoom'), ('G', 'Google Meets'), ('C', 'Cisco Webex')], default='')

    def validate_date(Form, field):
        if field.data < date.today():
            raise ValidationError("The date cannot be in the past!")


class CreateOEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired(), validators.Regexp('[a-zA-Z0-9_-]+$', message="It should only contain letters, numbers , underscores and dashes")])
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg' ,'gif'])])
    description = TextAreaField('Description', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    location = SelectField('Location', validators=[validators.DataRequired()], choices=[('Z', 'Zoom'), ('G', 'Google Meets'), ('C', 'Cisco Webex')], default='')
    event_status = SelectField('Event Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed'), ('O', 'Open-In-Advance')], default='O')
    reg_status = SelectField('Registration Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed')], default='O')

    def validate_date(Form, field):
        if field.data < date.today():
            raise ValidationError("The date cannot be in the past!")


class CreateOfflineEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired(), validators.Regexp('[a-zA-Z0-9_-]+$', message="It should only contain letters, numbers , underscores and dashes")])
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg' ,'gif'])])
    description = TextAreaField('Description', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    pax = IntegerField('Pax', [validators.NumberRange(min=0, max=1000, message="numbers should only range from 1 to 1000!"), validators.DataRequired()])
    location = StringField('Location', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired()])


    def validate_date(Form, field):
        if field.data < date.today():
            raise ValidationError("The date cannot be in the past!")


class CreateOffEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired(), validators.Regexp('[a-zA-Z0-9_-]+$', message="It should only contain letters, numbers , underscores and dashes")])
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg' ,'gif'])])
    description = TextAreaField('Description', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    pax = IntegerField('Pax', [validators.NumberRange(min=0, max=1000,message="numbers should only range from 1 to 1000!"), validators.DataRequired()])
    location = StringField('Location', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired()])
    event_status = SelectField('Event Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed'), ('O', 'Open-In-Advance')], default='O')
    reg_status = SelectField('Registration Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed')], default='O')

    def validate_date(Form, field):
        if field.data < date.today():
            raise ValidationError("The date cannot be in the past!")

