from datetime import date, datetime
from wtforms import Form, StringField, TextAreaField, validators, IntegerField, SelectField, ValidationError, \
    RadioField, DecimalField, SelectMultipleField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import EmailField, DateField, PasswordField
import re


class CreateEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150,message="It should be in a range from 1 to 150!"), validators.DataRequired(), validators.Regexp('[a-zA-Z0-9_-]+$', message="It should only contain letters, numbers , underscores and dashes")])
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    description = TextAreaField('Description', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    location = SelectField('Location', validators=[validators.DataRequired()], choices=[('Z', 'Zoom'), ('G', 'Google Meets'), ('C', 'Cisco Webex')], default='')

    def validate_date(Form, field):
        if field.data < date.today():
            raise ValidationError("The date cannot be in the past!")


class CreateOEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired(), validators.Regexp('[a-zA-Z0-9_-]+$', message="It should only contain letters, numbers , underscores and dashes")])
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg' ,'gif'])])
    description = TextAreaField('Description', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
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
    end_date = DateField('End Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
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
    end_date = DateField('End Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    pax = IntegerField('Pax', [validators.NumberRange(min=0, max=1000,message="numbers should only range from 1 to 1000!"), validators.DataRequired()])
    location = StringField('Location', [validators.Length(min=1, max=150, message="It should be in a range from 1 to 150!"), validators.DataRequired()])
    event_status = SelectField('Event Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed'), ('O', 'Open-In-Advance')], default='O')
    reg_status = SelectField('Registration Status', validators=[validators.DataRequired()], choices=[('A', 'Active'), ('C', 'Closed')], default='O')

    def validate_date(Form, field):
        if field.data < date.today():
            raise ValidationError("The date cannot be in the past!")


#trisven portion

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
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])

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
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])

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
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])

class UpdateCustomerForm(Form):
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
    image = FileField('Image', validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])

class RegisterEventForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phone_number = IntegerField('Phone Number', [validators.InputRequired(), check_phone_number])

    def check_phone_number(form, field):
        if not re.match(r'^[89][0-9]{7}$', str(field.data)):
            raise validators.ValidationError(
                'Invalid phone number,it must start with either 8 or 9 and be 8 digit long')

class ChangePassword(Form):
    password = PasswordField(validators=[validators.Length(min=8, message='Too short'), validators.DataRequired(), validators.Regexp(
            r'^(?=(.*[a-z]){3,})(?=(.*[A-Z]){2,})(?=(.*[0-9]){2,})(?=(.*[!@#$%^&*()\-__+.]){1,}).{8,}$',
            message="Invalid password. It must contain at least one uppercase letter, one lowercase letter, one digit, one special character and be at least 8 characters long.")])
    passwordcfm = PasswordField('', validators=[validators.EqualTo('password', 'Password mismatch')])

class Login(Form):
    email = EmailField('', [validators.Email(), validators.DataRequired()])
    password = PasswordField('', [validators.Length(min=1), validators.DataRequired()])


#azami

categories = ["All", "Ball", "Shoe", "Shin guards", "Shirt", "Shorts", "Socks"]


class CreateVoucherForm(Form):
    def validate_date(form, field):
        if field.data < datetime.date(datetime.now()):
            raise ValidationError("Date cannot be earlier than today's date")

    picture = SelectField("Image:", [validators.InputRequired()], choices=[("Logo.jpg", "Logo"), ("FreeShipping.jpg", "Free Shipping")])
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired(), validators.Regexp('^\w+', message="Voucher name must contain only letters numbers or underscore")])
    type = SelectField("Type of voucher", [validators.DataRequired()], choices=[("$", "$"), ("%", "%"), ("Gift", "Free")])
    amount = IntegerField('Amount off', [validators.NumberRange(min=0), validators.InputRequired()], render_kw={'style': 'width: 8ch'})
    min_spend = IntegerField('Min. spend ($)', [validators.InputRequired(), validators.NumberRange(min=0)], render_kw={'style': 'width: 8ch'})
    category = StringField('Category', [validators.Length(min=1, max=150), validators.DataRequired(), validators.AnyOf(categories)])
    start = DateField('Start date', [validators.DataRequired()], format='%Y-%m-%d', default=datetime.now, render_kw={'style': 'width: 20ch'})
    expiry = DateField('Expiry date', [validators.DataRequired(), validate_date], format='%Y-%m-%d', default=datetime.now, render_kw={'style': 'width: 20ch'})
    description = TextAreaField('Description', [validators.Optional(), validators.Length(min=1, max=150), validators.Regexp('^\w+', message="Voucher name must contain only letters numbers or underscore")])
    status = SelectField("Type of voucher", [validators.DataRequired()], choices=[("Active", "Active"), ("Inactive", "Inactive")])

    def validate(self, **kwargs):
        # Standard validators
        rv = Form.validate(self)
        # Ensure all standard validators are met
        if rv:
            # Ensure end date >= start date
            if self.start.data > self.expiry.data:
                self.expiry.errors.append('Expiry date must be set after the starting date.')
                return False

            return True

        return False

#rayden

class CreateProduct(Form):
    name = StringField('Name: ', [validators.DataRequired()])
    desc = TextAreaField('Description: ', [validators.Optional()])
    price = DecimalField('Price: ', [validators.DataRequired()])
    qty = IntegerField('Quantity: ', [validators.InputRequired()])
    grp = SelectMultipleField("Category: ",[validators.DataRequired()], choices=[('Shoes','Shoes'),('Shirts','Shirts',),('Pants','Pants'),('Accessories','Accessories')])
    image = FileField('Image: ',validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    sale = SelectField('Sale Status:', validators=[validators.DataRequired()], choices=[('Active', 'Active'), ('Inactive', 'Inactive')],default='Inactive')

class UpdateProduct(Form):
    name = StringField('Name: ', [validators.DataRequired()])
    desc = TextAreaField('Description: ', [validators.Optional()])
    price = DecimalField('Price: ', [validators.DataRequired()])
    qty = IntegerField('Quantity: ', [validators.InputRequired()])
    grp = SelectMultipleField("Category: ",[validators.DataRequired()], choices=[('Shoes','Shoes'),('Shirts','Shirts',),('Pants','Pants'),('Accessories','Accessories')])
    sale = RadioField('Enable sale?:', validators=[validators.DataRequired()], choices=[('Yes','Yes'),('No','No')],default='No')
    status = SelectField('Product Status: ',[validators.DataRequired()], choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    sale = SelectField('Sale Status:', validators=[validators.DataRequired()], choices=[('Active', 'Active'), ('Inactive', 'Inactive')],default='Inactive')

class UpdateProductSale(Form):
    salestartdate = DateField('Sale start date:',validators = [validators.DataRequired()],format='%Y-%m-%d')
    saleenddate = DateField('Sale end date:',validators = [validators.DataRequired()],format='%Y-%m-%d')
    saleprice = DecimalField('Sale percentage:',validators = [validators.DataRequired()])
    def validate_saleenddate(form, field):
        if field.data < form.salestartdate.data:
            raise ValidationError("End date must not be earlier than start date.")
    def validate_salestartdate(form, field):
        if field.data < date.today():
            raise ValidationError("The start date cannot be in the past.")

class UpdateProductImg(Form):
    image = FileField('Image: ',validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])

class PurchaseProduct(Form):
    qty = IntegerField('Quantity: ', [validators.InputRequired()])
    option = RadioField('Choose Checkout:', validators=[validators.DataRequired()], choices=[('Purchase','Purchase'),('Add to cart','Add to cart')],default='No')


