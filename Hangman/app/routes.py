from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Word
from flask import flash, g, jsonify, redirect, render_template, request, session, url_for
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
def hangman():
    # TODO: Move this to an app variable instead of a session variable
    session['global_words'] = [ w.word for w in Word.query.all()]
    return render_template('hangman.html', title='Hangman')


@app.route('/')
@app.route('/index')
@login_required
def index():
    highscores = [ {u.username: u.highscore} for u in  User.query.all() ]
    print highscores
    return render_template('index.html', title='Home', highscores=highscores)


@app.route('/new_word')
@login_required
def new_word():
    current_word = choice(session['global_words'])
    response = { 'word_size': len(current_word), 'score': 60 }
    session['word'] = current_word
    session.modified = True
    session['attempted_word'] = '_' * len(current_word)
    session.modified = True
    session['score'] = 60
    return jsonify(response)


@app.route('/character', methods=['GET', 'POST'])
@login_required
def character():
    if session.get('word', '') == '':
        new_word()
    c = request.args.get('c')
    response = {}
    if c not in string.ascii_lowercase and c not in string.digits:
        response = {'error': 1, 'error_message': 'Invalid character'}
    elif c not in session['word']:
        session['score'] -= 10
        response = {'error': 0, 'error_message': 'OK', 'found': 0, 'word': session['attempted_word'], 'score': session['score'], 'winner': 0}
    else:
        partial_unmasked_word = partial_unmask(
            session['word'], session['attempted_word'], c)
        if partial_unmasked_word == session['word']:
            response = {'error': 0, 'error_message': 'OK', 'found': 1, 'word': partial_unmasked_word, 'score': session['score'], 'winner': 1}
            save_score_if_higher(session['score'])
        else:
            response = {'error': 0, 'error_message': 'OK', 'found': 1, 'word': partial_unmasked_word, 'score': session['score'], 'winner': 0}

    return jsonify(response)

def partial_unmask(word, attempted_word, character):
    if attempted_word == "":
        attempted_word = '_' * len(word)

    new_attempt = ''
    for i in range(0, len(word)):
        if word[i] == character:
            new_attempt += word[i]
        else:
            new_attempt += attempted_word[i]
    session['attempted_word'] = new_attempt
    return new_attempt

def save_score_if_higher(score):
    # You never know
    if current_user.is_authenticated:
        if current_user.highscore < score:
            current_user.highscore = score
            db.session.commit()
