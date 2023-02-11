from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField, RadioField
import re

#remove add product


#validation address

def check_phone_number(form, field):
    if not re.match(r'^[56789][0-9]{7}$', str(field.data)):
        raise validators.ValidationError('Invalid phone number,it must start with either 8 or 9 and be 8 digit long')

def check_postal_code(form, field):
    if not re.match(r'[0-9]{6}$', str(field.data)):
        raise validators.ValidationError('Invalid postal code. It must be 6 digit long')

def check_payment(form, field):
    if not re.match(r'[0-9]{16}$', str(field.data)):
        raise validators.ValidationError('Invalid card details. It must be 16 digit long')

def check_floor_number(form, field):
    if not re.match(r'\d{1,2}$', str(field.data)):
         raise validators.ValidationError('No floor number has been entered, it must be 2 digit long')
def check_unit_number(form, field):
    if not re.match(r'\d{3}$', str(field.data)):
         raise validators.ValidationError('No Unit number has been entered, it must be 3 digit long')
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
    Qty = IntegerField('Quantity: ',[validators.NumberRange(min=1,max=1000),validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])
    status = RadioField('Status',[validators.DataRequired()], choices=[('Available', 'Available'), ('Not Available', 'Not available')], default='')




