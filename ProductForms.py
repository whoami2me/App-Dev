from wtforms import Form, StringField, RadioField, SelectMultipleField, TextAreaField, DecimalField,IntegerField,validators
 
class CreateProduct(Form):
    name = StringField('Name: ', [validators.DataRequired()])
    desc = TextAreaField('Description: ', [validators.Optional()])
    price = DecimalField('Price: ', [validators.DataRequired()])
    qty = IntegerField('Quantity: ', [validators.DataRequired()])
    grp = SelectMultipleField("Category: ",[validators.DataRequired()], choices=[('Shoes','Shoes'),('Shirts','Shirts',),('Pants','Pants'),('Accessories','Accessories')])