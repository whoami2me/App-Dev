from wtforms import Form, TextAreaField, validators, IntegerField


class CreateInventoryForm(Form):

    Qty = IntegerField('Quantity: ', [validators.NumberRange(min=1, max=1000), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])
