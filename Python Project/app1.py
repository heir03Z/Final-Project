# encoding=utf8

"""
2021/03/02
"""

from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, AddForm
from flask_login import UserMixin
from datetime import datetime
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

class Sentences(db.Model):
    __tablename__ = 'sentences'
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String(1000))
    pub_date = db.Column(db.DateTime)

    # Initializes the fields with entered data
    def __init__(self, sentence):
        self.sentence = sentence
        self.pub_date = datetime.now()

with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    """
    Index Page
    """
    return render_template('index.html', sentences=Sentences.query.order_by(Sentences.pub_date.asc()).all())

@app.route('/create', methods=['POST', 'GET'])
def create():
    """
    page for creating the story
    """
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        sentence = Sentences(sentence=form.sentence.data)
        db.session.add(sentence)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', form = form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Create a registration page"""
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('The account is created, please log in')
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
