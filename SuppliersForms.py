from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField
import re

#remove add product


#validation address

def check_phone_number(form, field):
    if not re.match(r'^[6789][0-9]{7}$', str(field.data)):
        raise validators.ValidationError('Invalid phone number,it must start with either 8 or 9 and be 8 digit long')

def check_postal_code(form, field):
    if not re.match(r'[0-9]{6}$', str(field.data)):
        raise validators.ValidationError('Invalid postal code. It must be 6 digit long')

def check_payment(form, field):
    if not re.match(r'[0-9]{16}$', str(field.data)):
        raise validators.ValidationError('Invalid card details. It must be 16 digit long')
class CreateSuppliersForm(Form):
    Company_name = StringField('Company Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    telephone = IntegerField('Phone Number', [validators.InputRequired(), check_phone_number])
    website = StringField('Supplier website', [validators.Length(min=1, max=150), validators.DataRequired(), validators.regexp("^https://[0-9A-z.]+.[0-9A-z.]+.[a-z]+$",message= "Please enter a valid website")])
    email = StringField('Company e-mail:', [validators.Email(message="Please enter a valid email")])
    Address1 = StringField('Address line 1', [validators.Length(min=1, max=150), validators.DataRequired()])
    Address2 = StringField('Unit no.', [validators.Length(min=1, max=10), validators.Optional()])
    postal = IntegerField('Postal code', [validators.InputRequired(), check_postal_code])
    Payment = IntegerField("Payment Details", [validators.InputRequired(), check_payment])
    Categories_select = SelectField('Categories', [validators.DataRequired()], choices=[('', 'Select'), ('B', 'Ball'), ('F', 'Footwear')],default='')
    Product_name = StringField('Name of product', [validators.Length(min=1, max=150), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])



    # membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
