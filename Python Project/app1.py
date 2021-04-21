# encoding=utf8

"""
2021/03/02
"""

from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, SubmitField, validators
from flask_login import UserMixin
import os

# create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'


# create a database to store user information
db = SQLAlchemy()
DB_NAME = 'database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25))

    def __repr__(self):
        return '<User %r>' % self.username

with app.app_context():
    db.create_all()

DB_FILE = "Python Project/data/story.txt"

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    psw = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='password must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    psw = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Log in')

    
@app.route('/')
def index():
    """
    Index Page
    """


    return render_template('index(2).html')

@app.route('/create', methods=['POST', 'GET'])
def create():
    """
    page for creating the story
    """
    lines = []
    with open(DB_FILE, 'r', encoding='utf8') as f:
        for line in f:
            lines.append(line.strip())

    return render_template('create.html', lines=lines)


@app.route('/save', methods=['POST'])
def save():
    """
    save next sentence
    """
    f = request.form
    sentence = f['sentence']

    # strip heading and trailing blanks
    sentence = sentence.strip()
    print('====== new sentence:', sentence)

    # append to file
    with open(DB_FILE, 'a', encoding='utf8') as f:
        f.write(sentence + '\n')

    # go back to index page
    return redirect(url_for('create', name='test'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    """Create a registration page"""
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('The account is created')
        new_user = User(username=form.username.data, password=form.psw.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Create a login page"""
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.psw.data:
                return redirect(url_for('create'))
    return render_template('login.html', form = form)





# main
if __name__ == '__main__':
    app.run(debug=True)
