from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField
from wtforms.fields import DateField
from datetime import datetime


list = ["All", "Ball", "Shoe"]
special = "^(?=.*[-+_!@#$%^&*., ?])"


class CreateVoucherForm(Form):

    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired(), validators.NoneOf(special)])
    amount = IntegerField('Amount off', [validators.NumberRange(min=1, max=100, message='Invalid value, min is 1 and max is 100.'), validators.DataRequired()], render_kw={'style': 'width: 8ch'})
    type = SelectField("$ / %", choices=[("$", "$"), ("%", "%")], render_kw={'style': 'width: 5ch'})
    category = StringField('Category', [validators.Length(min=1, max=150), validators.DataRequired(), validators.AnyOf(list)])
    start = DateField('Start date', [validators.DataRequired()], format='%Y-%m-%d', default=datetime.now, render_kw={'style': 'width: 20ch'})
    expiry = DateField('Expiry date', [validators.DataRequired()], format='%Y-%m-%d', default=datetime.now, render_kw={'style': 'width: 20ch'})
    description = TextAreaField('Description', [validators.Optional(), validators.NoneOf(special)])
