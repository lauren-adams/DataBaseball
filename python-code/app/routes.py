from flask import render_template, redirect, request, url_for, session
from app import app
from app.daos.user_dao import save_user
from app.models.user import User
from app.validator import validate_login, validate_signup
import app.util.encrypt as encrypt

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template('index.html', username=username)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    args = request.args

    # display login page
    if request.method == 'GET':
        error = args.get('error') if 'error' in args else None
        return render_template('login.html', error=error)

    # handle login logic
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # input validation
        error = validate_login(username, password)
        if error:
            return redirect(url_for('login', error=error))

        # save login info to session
        session['username'] = username

        return redirect(url_for('index'))


@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    args = request.args

    # display signup page
    if request.method == 'GET':
        error = args.get('error') if 'error' in args else None
        return render_template('signup.html', error=error)

    # handle signup logic
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        passwordConfirmation = request.form.get('passwordConfirmation')

        # input validation
        error = validate_signup(username, password, passwordConfirmation)
        if error:
            return redirect(url_for('signup', error=error))

        # save login info to session
        session['username'] = username

        # save the user to the database
        user = User(username, encrypt.sha1(password))
        save_user(user)

        return redirect(url_for('index'))

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))
