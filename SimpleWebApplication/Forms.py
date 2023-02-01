from datetime import date
from wtforms import Form, StringField, TextAreaField, validators, IntegerField, SelectField, ValidationError, RadioField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import EmailField, DateField, PasswordField
import re


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


#trisven membership portion
def check_phone_number(form, field):
    if not re.match(r'^[89][0-9]{7}$', str(field.data)):
        raise validators.ValidationError('Invalid phone number,it must start with either 8 or 9 and be 8 digit long')
def check_postal_code(form, field):
    if not re.match(r'^[1-9][0-9]{5}$', str(field.data)):
         raise validators.ValidationError('Invalid Postal Code, it must be 6 digit long')

def check_floor_number(form, field):
    if not re.match(r'\d{1,2}$', str(field.data)):
         raise validators.ValidationError('No floor number has been entered, it must be 2 digit long')

def check_unit_number(form, field):
    if not re.match(r'\d{3}$', str(field.data)):
         raise validators.ValidationError('No Unit number has been entered, it must be 3 digit long')

class CreateStaffForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message='First Name is empty')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(message='Last Name is empty')])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address1 = StringField('Address Line 1', [validators.length(max=100), validators.DataRequired()])
    address2 = StringField('Address Line 2 (Optional)', [validators.length(max=100)])
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
    phone_number = IntegerField('Phone Number', [validators.InputRequired(), check_phone_number])
    postal_code = IntegerField('Postal Code', [validators.input_required(), check_postal_code])
    floor_number = IntegerField('#', [validators.input_required(), check_floor_number])
    unit_number = IntegerField('-', [validators.input_required(), check_unit_number])

class UpdateStaffForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message='First Name is empty')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(message='Last Name is empty')])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address1 = StringField('Address Line 1', [validators.length(max=100), validators.DataRequired()])
    address2 = StringField('Address Line 2 (Optional)', [validators.length(max=100)])
    membership = SelectField('Membership', choices=[('Employee', 'Employee'), ('Admin', 'Admin')], default='Employee')
    phone_number = IntegerField('Phone Number', [validators.InputRequired(), check_phone_number])
    postal_code = IntegerField('Postal Code', [validators.input_required(), check_postal_code])
    floor_number = IntegerField('#', [validators.input_required(), check_floor_number])
    unit_number = IntegerField('-', [validators.input_required(), check_unit_number])
    status = RadioField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

class UpdateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address1 = StringField('Address Line 1', [validators.length(max=100), validators.DataRequired()])
    address2 = StringField('Address Line 2 (Optional)', [validators.length(max=100)])
    phone_number = IntegerField('Phone Number', [validators.InputRequired(), check_phone_number])
    postal_code = IntegerField('Postal Code', [validators.input_required(), check_postal_code])
    floor_number = IntegerField('#', [validators.input_required(), check_floor_number])
    unit_number = IntegerField('-', [validators.input_required(), check_unit_number])
    status = RadioField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')


#de register events

class RegisterEventForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phone_number = IntegerField('Phone Number', [validators.InputRequired(), check_phone_number])


#izwan
def check_payment(form, field):
    if not re.match(r'[0-9]{16}$', str(field.data)):
        raise validators.ValidationError('Invalid card details. It must be 16 digit long')


class CreateSuppliersForm(Form):
    Company_name = StringField('Company Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    telephone = IntegerField('Phone Number', [validators.InputRequired(), check_phone_number])
    website = StringField('Supplier website', [validators.Length(min=1, max=150), validators.DataRequired(), validators.regexp("^https://[0-9A-z.]+.[0-9A-z.]+.[a-z]+$",message= "Please enter a valid website")])
    email = StringField('Company e-mail:', [validators.Email(message="Please enter a valid email")])
    Address1 = StringField('Address line', [validators.Length(min=1, max=150), validators.DataRequired()])
    floor_number = IntegerField('#', [validators.optional(), check_floor_number])
    unit_number = IntegerField('-', [validators.optional(), check_unit_number])
    postal = IntegerField('Postal code', [validators.InputRequired(), check_postal_code])
    Payment = IntegerField("Payment Details", [validators.InputRequired(), check_payment])
    Categories_select = SelectField('Categories', [validators.DataRequired()], choices=[('', 'Select'), ('Ball', 'Ball'), ('Footwear', 'Footwear'),('Shirts','Shirts',),('Pants','Pants'),('Accessories','Accessories')],default='')
    Product_name = StringField('Name of product', [validators.Length(min=1, max=150), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])


class CreateInventoryForm(Form):
    Categories_select = SelectField('Categories', [validators.DataRequired()], choices=[('', 'Select'), ('B', 'Ball'), ('F', 'Footwear')],default='')
    Product_name = StringField('Name of product', [validators.Length(min=1, max=150), validators.DataRequired()])
    Qty = IntegerField('Quantity: ',[validators.NumberRange(min=1,max=100),validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])
