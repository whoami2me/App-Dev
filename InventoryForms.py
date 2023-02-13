from wtforms import Form, SelectField, TextAreaField, validators, IntegerField
import shelve

class CreateInventoryForm(Form):
    Suppliers_dict = {}
    db = shelve.open('supplier.db', 'r')
    try:
        Suppliers_dict = db['Supplier']
    except:
        print("Error in retrieving Users from supplier.db for closing")
    db.close()

    supplier_choices = [('', 'Select')]
    type_choices = [('', 'Select')]
    product_name_choices = [('', 'Select')]

    for key in Suppliers_dict:
        supplier = Suppliers_dict.get(key)
        supplier_choices.append((supplier.get_Company_name(), supplier.get_Company_name()))
        type_choices.append((supplier.get_Categories_select(), supplier.get_Categories_select()))
        product_name_choices.append((supplier.get_Product_name(), supplier.get_Product_name()))

    name = SelectField('Company name: ', [validators.DataRequired()], choices=supplier_choices, default='')
    type = SelectField('Categories: ', [validators.DataRequired()], choices=type_choices, default='')
    Product_name = SelectField('Name of product: ', [validators.DataRequired()], choices=product_name_choices, default='')
    Qty = IntegerField('Quantity: ', [validators.NumberRange(min=1, max=1000), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])
