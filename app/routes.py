from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User         # this also imports the UserMixins

@app.route('/')
@app.route('/index')
@login_required            # following function is protected by login page
                           # when user surfs to /index, the decorator will intercept the request
                           # and respond with a redirect to /login and will add a query string
                           # to the URL as follows: /login?next=/index
def index():
	posts = [
        {
            'author': {'username':'John'},
            'body': 'Beautiful day in Singapore'
        },
        {
        	'author': {'username': 'Susan'},
        	'body': 'The Avengers movie was so cool!'
        }
	]
	return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:        # getting current_user from Flask_Login
        return redirect(for_url('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # if user is validated, grab the user
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
            return redirect(url_for('login'))

    	# login_user function comes from Flask_Login
    	#    and will register the user as logged in, so in future pages the user will
    	#    have the current_user variable set that to the user
        login_user(user, remember=form.remember_me.data)        # getting login_user from Flask_Login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	# logout_user function comes from Flask_Login
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You\'re now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
