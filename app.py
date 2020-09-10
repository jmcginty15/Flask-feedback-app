from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yeet'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    return redirect('/register')

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('registration-form.html', form=form)

@app.route('/register', methods=['POST'])
def register_process():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = new_user.username
        return redirect('/secret')
    else:
        return render_template('registration-form.html', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login-form.html', form=form)

@app.route('/login', methods=['POST'])
def login_process():
    form = LoginForm()
    print(form.validate_on_submit(), flush=True)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username=username, password=password)
        if user:
            session['user'] = user.username
            return redirect('/secret')
        else:
            flash('Incorrect username or password!')
            return render_template('login-form.html', form=form)
    else:
        return redirect('/')

@app.route('/secret')
def secret():
    if session.get('user'):
        return 'You made it!'
    else:
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session.pop('user')
    flash('Logged out!')
    return redirect('/')
