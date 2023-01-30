from wtforms import Form, StringField, FileField, SelectMultipleField, TextAreaField, DecimalField,IntegerField,validators,SelectField,RadioField
from flask_wtf.file import FileAllowed
class CreateProduct(Form):
    name = StringField('Name: ', [validators.DataRequired()])
    desc = TextAreaField('Description: ', [validators.Optional()])
    price = DecimalField('Price: ', [validators.DataRequired()])
    qty = IntegerField('Quantity: ', [validators.DataRequired()])
    grp = SelectMultipleField("Category: ",[validators.DataRequired()], choices=[('Shoes','Shoes'),('Shirts','Shirts',),('Pants','Pants'),('Accessories','Accessories')])
    image = FileField('Image: ',validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    sale = RadioField('Enable sale?:', validators=[validators.DataRequired], choices=[('Yes','Yes'),('No','No')],default='No')

class UpdateProduct(Form):
    name = StringField('Name: ', [validators.DataRequired()])
    desc = TextAreaField('Description: ', [validators.Optional()])
    price = DecimalField('Price: ', [validators.DataRequired()])
    qty = IntegerField('Quantity: ', [validators.DataRequired()])
    grp = SelectMultipleField("Category: ",[validators.DataRequired()], choices=[('Shoes','Shoes'),('Shirts','Shirts',),('Pants','Pants'),('Accessories','Accessories')])
    image = FileField('Image: ',validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    sale = RadioField('Enable sale?:', validators=[validators.DataRequired], choices=[('Yes','Yes'),('No','No')],default='No')
    status = SelectField('Status: ',[validators.DataRequired()], choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
