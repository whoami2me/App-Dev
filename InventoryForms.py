from wtforms import Form, TextAreaField, validators, IntegerField


class CreateInventoryForm(Form):

    Order_Qty = IntegerField('Quantity: ', [validators.NumberRange(min=1, max=1000), validators.DataRequired()])
    Order_remarks = TextAreaField('Remarks', [validators.Optional()])
