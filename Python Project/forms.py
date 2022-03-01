from wtforms import Form, StringField, PasswordField, SubmitField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    psw = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='password must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    psw = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Log in')

class AddForm(Form):
    sentence = StringField('Sentence', [validators.Length(min=1, max=1000)])
    submit = SubmitField('Add')