from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, ValidationError, IntegerField
from wtforms.fields import EmailField, DateField, PasswordField
import re


def check_phone_number(form, field):
    if not re.match(r'^[89][0-9]{7}$', str(field.data)):
        raise validators.ValidationError('Invalid phone number,it must start with either 8 or 9 and be 8 digit long')
def check_postal_code(form, field):
    if not re.match(r'^[1-9][0-9]{5}$', str(field.data)):
         raise validators.ValidationError('Invalid Postal Code, it must be 6 digit long')

def check_floor_number(form, field):
    if not re.match(r'^[0-9][0-9]{0}$', str(field.data)):
         raise validators.ValidationError('No floor number has been entered, it must be 2 digit long')

def check_unit_number(form, field):
    if not re.match(r'^[0-9][0-9]{2}$', str(field.data)):
         raise validators.ValidationError('No Unit number has been entered, it must be 2 digit long')

class CreateStaffForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message='First Name is empty')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(message='Last Name is empty')])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address1 = StringField('Address Line 1', [validators.length(max=100), validators.DataRequired()])
    address2 = StringField('Address Line 2 (Optional)', [validators.length(max=100)])
    membership = SelectField('Membership', choices=[('E', 'Employee'), ('A', 'Admin')], default='F')
    password = PasswordField(validators=[validators.Length(min=8, message='Too short'), validators.DataRequired(), validators.Regexp(
        r'^(?=(.*[a-z]){3,})(?=(.*[A-Z]){2,})(?=(.*[0-9]){2,})(?=(.*[!@#$%^&*()\-__+.]){1,}).{8,}$',
        message="Invalid password. It must contain at least one uppercase letter, one lowercase letter, one digit, one special character and be at least 8 characters long.")])
    passwordcfm = PasswordField('Confirm Password', validators=[validators.EqualTo('password', 'Password mismatch')])
    phone_number = IntegerField('Phone Number', [validators.InputRequired(), check_phone_number])
    postal_code = IntegerField('Postal Code', [validators.input_required(), check_postal_code])
    floor_number = IntegerField('#', [validators.input_required(), check_floor_number])
    unit_number = IntegerField('-', [validators.input_required(), check_unit_number])

class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address1 = StringField('Address Line 1', [validators.length(max=100), validators.DataRequired()])
    address2 = StringField('Address Line 2 (Optional)', [validators.length(max=100)])
    password = PasswordField(validators=[validators.Length(min=8, message='Too short'), validators.DataRequired(), validators.Regexp(
            r'^(?=(.*[a-z]){3,})(?=(.*[A-Z]){2,})(?=(.*[0-9]){2,})(?=(.*[!@#$%^&*()\-__+.]){1,}).{8,}$',
            message="Invalid password. It must contain at least one uppercase letter, one lowercase letter, one digit, one special character and be at least 8 characters long.")])
    passwordcfm = PasswordField('Confirm Password', validators=[validators.EqualTo('password', 'Password mismatch')])

    def check_phone(form, field):
        if not re.match(r'^[89][0-9]{7}$', str(field.data)):
            raise validators.ValidationError(
                'Invalid phone number,it must start with either 8 or 9 and be 8 digit long')

    phone_number = IntegerField('Phone Number', [validators.InputRequired(), check_phone])

class UpdateStaffForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message='First Name is empty')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(message='Last Name is empty')])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address1 = StringField('Address Line 1', [validators.length(max=100), validators.DataRequired()])
    address2 = StringField('Address Line 2 (Optional)', [validators.length(max=100)])
    membership = SelectField('Membership', choices=[('E', 'Employee'), ('A', 'Admin')], default='F')
    phone_number = IntegerField('Phone Number', [validators.InputRequired(), check_phone_number])
    postal_code = IntegerField('Postal Code', [validators.input_required(), check_postal_code])
    floor_number = IntegerField('#', [validators.input_required(), check_floor_number])
    unit_number = IntegerField('-', [validators.input_required(), check_unit_number])
    status = RadioField('Status', choices=[('A', 'Active'), ('I', 'Inactive')], default='A')