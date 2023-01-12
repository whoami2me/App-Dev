from wtforms import Form, StringField, SelectField, TextAreaField, validators, DateField , IntegerField, EmailField


class CreateOnlineEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')


class CreateOfflineEventForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    date = DateField('Date', validators=[validators.DataRequired()], format='%Y-%m-%d')
    pax = IntegerField('Pax', [validators.NumberRange(min=0, max=200), validators.DataRequired()])


class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    address1 = StringField('Address Line 1', [validators.length(max=100), validators.DataRequired()])
    address2 = StringField('Address Line 2', [validators.length(max=100), validators.DataRequired()])
    membership = SelectField('Membership', choices=[('P', 'User'), ('C', 'Customer')], default='')
