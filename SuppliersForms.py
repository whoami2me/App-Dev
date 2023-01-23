from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField


class CreateSuppliersForm(Form):
    Company_name = StringField('Company Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    telephone = IntegerField('Telephone No.', [validators.NumberRange(min=11111111, max=99999999, message="Integer must have 8 digits"), validators.DataRequired()])
    website = StringField('Supplier website', [validators.Length(min=1, max=150), validators.DataRequired()])
    Address1 = StringField('Address line 1', [validators.Length(min=1, max=150), validators.DataRequired()])
    Address2 = StringField('Address line 2', [validators.Length(min=1, max=10), validators.DataRequired()])
    Payment = IntegerField("Payment Details", [validators.NumberRange(min=1111111111111111, max=9999999999999999, message="Integer must have 16 digits"), validators.DataRequired()])
    Categories_select = SelectField('Categories', [validators.DataRequired()], choices=[('', 'Select'), ('B', 'Ball'), ('F', 'Footwear')],default='')
    Product_name = StringField('Name of product', [validators.Length(min=1, max=150), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])


    # membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
