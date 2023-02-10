from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField

class CreateInventoryForm(Form):

    Categories_select = SelectField('Categories: ', [validators.DataRequired()], choices=[('', 'Select'), ('Ball', 'Ball'), ('Footwear', 'Footwear'),('Shirts','Shirts',),('Pants','Pants'),('Accessories','Accessories')],default='')
    Product_name = StringField('Name of product: ', [validators.Length(min=1, max=150), validators.DataRequired()])
    Qty = IntegerField('Quantity: ',[validators.NumberRange(min=1,max=1000),validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])
