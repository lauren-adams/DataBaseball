from flask import render_template, redirect, request, url_for, session
from app import app
from app.daos.user_dao import save_user, getAllUsers
from app.daos.search_dao import search_teamYear, getYears, getTeams, getDiv, getPlayOffs, inPlayOffs, getWinner
from app.models.user import User
from app.validator import validate_login, validate_signup
import app.util.encrypt as encrypt
from logging.config import dictConfig

# configure logger to write to log file
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "flask.log",
                "formatter": "default",
            },
        },
        "root": {"level": "INFO", "handlers": ["console", "file"]},
    }
)


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    if username == "admin":
        # renders admin only view
        return render_template('index_admin.html', username=username)
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

'''
function: search()
return: rendered search page or the results
displays teams and years and if submit is clicked it displays results to screen
'''
@app.route('/search', methods=['GET', 'POST'])
def search():
    # displays results
    if request.method == "POST":
        # logs searches by user
        app.logger.info(session['username'] + " is searching " + request.form.get('year') + " " + request.form.get('team'))
        params = [request.form.get('year'), request.form.get('team')]
        results = search_teamYear(params)
        # get division that matches the team and year
        div = getDiv(params)
        po = ""
        win = ""
        # if in playoffs it displays playoff data
        if inPlayOffs(params) == 1:
            po = getPlayOffs(request.form.get('year'))
            win = getWinner(request.form.get('year'))
        return render_template("results.html", records=results, year=request.form.get('year'), team=request.form.get('team'), division= div, playoffs= po, winner= win)
    # renders teams and years to the screen
    team = getTeams()
    year = getYears()
    return render_template('search.html', teams= team, years= year)

'''
function: users()
return: rendered user page
displays all saved users
'''
@app.route('/users', methods=['POST', 'GET'])
def users():
    args = request.args
    # return to home
    if request.method == 'POST':
        error = args.get('error') if 'error' in args else None
        return render_template('index_admin.html', error=error)

    # handle displaying users logic
    if request.method == 'GET':
        app.logger.info(session['username'] + " is viewing user data")

    all_users = getAllUsers()

    return render_template('users.html', users=all_users)
