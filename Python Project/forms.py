from wtforms import Form, StringField, PasswordField, SubmitField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    psw = PasswordField('Password', [validators.DataRequired(),
    validators.EqualTo('psw-repeat', message='password must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    psw = PasswordField('Password', [validators.DataRequired()])
