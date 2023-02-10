from wtforms import Form, StringField, FileField, SelectMultipleField, TextAreaField, DecimalField,IntegerField,validators,SelectField,RadioField, ValidationError
from flask_wtf.file import FileAllowed
from wtforms.fields import DateField
from datetime import date
class CreateProduct(Form):
    name = StringField('Name: ', [validators.DataRequired()])
    desc = TextAreaField('Description: ', [validators.Optional()])
    price = DecimalField('Price: ', [validators.DataRequired()])
    qty = IntegerField('Quantity: ', [validators.DataRequired()])
    grp = SelectMultipleField("Category: ",[validators.DataRequired()], choices=[('Shoes','Shoes'),('Shirts','Shirts',),('Pants','Pants'),('Accessories','Accessories')])
    image = FileField('Image: ',validators=[validators.DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    sale = RadioField('Enable sale?:', validators=[validators.DataRequired()], choices=[('Yes','Yes'),('No','No')],default='No')

class UpdateProduct(Form):
    name = StringField('Name: ', [validators.DataRequired()])
    desc = TextAreaField('Description: ', [validators.Optional()])
    price = DecimalField('Price: ', [validators.DataRequired()])
    qty = IntegerField('Quantity: ', [validators.DataRequired()])
    grp = SelectMultipleField("Category: ",[validators.DataRequired()], choices=[('Shoes','Shoes'),('Shirts','Shirts',),('Pants','Pants'),('Accessories','Accessories')])
    sale = RadioField('Enable sale?:', validators=[validators.DataRequired()], choices=[('Yes','Yes'),('No','No')],default='No')
    status = SelectField('Status: ',[validators.DataRequired()], choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    sale = RadioField('Enable sale?:', validators=[validators.DataRequired()], choices=[('Yes','Yes'),('No','No')],default='No')

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
