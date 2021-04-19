# encoding=utf8

"""
2021/03/02
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

DB_FILE = "./data/db.txt"

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
    return render_template('register.html', form = form)
    if request.method == 'POST' and form.validate():
        flash('The account is created')
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Create a login page"""
    form = LoginForm()
   
    if request.method == 'POST' and form.validate():
        return render_template('create.html')

    return render_template('login.html', form = form)





# main
if __name__ == '__main__':
    app.run(debug=True)
