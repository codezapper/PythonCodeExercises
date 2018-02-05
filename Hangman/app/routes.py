from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask import flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from random import choice
import string

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/hangman')
@login_required
def main_game():
    return render_template('hangman.html', title='Hangman')


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/new_word')
@login_required
def new_word():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    possible_words = ['3dhubs', 'marvin',
                      'print', 'filament', 'order', 'layer']
    current_word = choice(possible_words)
    response = { 'word_size': len(current_word) }
    session['word'] = current_word
    session['attempted_word'] = '_' * len(current_word)
    return jsonify(response)


@app.route('/character', methods=['GET', 'POST'])
@login_required
def character():
    print session.get('word', '')
    if session.get('attempted_word', '') == '':
        new_word()
    ch = request.args.get('c')
    response = {}
    if ch not in string.ascii_lowercase:
        response = {'error': 1, 'error_message': 'Invalid character'}
    elif ch not in session['word']:
        response = {'found': 0, 'word': session['attempted_word']}
    else:
        response = {'found': 1, 'word': partial_unmask(session['word'], session['attempted_word'], ch)}

    return jsonify(response)

def partial_unmask(word, attempted_word, character):
    new_attempt = ''
    for i in range(0, len(word)):
        if word[i] == character:
            new_attempt += word[i]
        else:
            new_attempt += attempted_word[i]
    session['attempted_word'] = new_attempt
    return new_attempt
