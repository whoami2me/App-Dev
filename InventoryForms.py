from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField

class CreateInventoryForm(Form):

    Categories_select = SelectField('Categories', [validators.DataRequired()], choices=[('', 'Select'), ('B', 'Ball'), ('F', 'Footwear')],default='')
    Product_name = StringField('Name of product', [validators.Length(min=1, max=150), validators.DataRequired()])
    Qty = IntegerField('Quantity: ',[validators.NumberRange(min=1,max=100),validators.DataRequired])
    remarks = TextAreaField('Remarks', [validators.Optional()])
