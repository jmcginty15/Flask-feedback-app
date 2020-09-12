from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegistrationForm, LoginForm, FeedbackSubmissionForm

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
    return render_template('home.html')

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
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('registration-form.html', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login-form.html', form=form)

@app.route('/login', methods=['POST'])
def login_process():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username=username, password=password)
        if user:
            session['user'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            flash('Incorrect username or password!')
            return render_template('login-form.html', form=form)
    else:
        return redirect('/')

@app.route('/users/<username>')
def secret(username):
    user = User.query.filter_by(username=username).first()
    logged_in_username = session.get('user')
    if logged_in_username == user.username:
        return render_template('logged-in-user.html', user=user)
    else:
        flash(f'You must be logged in as {username} to access that page!')
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session.pop('user')
    flash('Logged out!')
    return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    logged_in_username = session.get('user')
    if logged_in_username == user.username:
        session.pop('user')
        db.session.delete(user)
        db.session.commit()
        flash(f'Deleted {username}!')
        return redirect('/')
    else:
        flash(f'You must be logged in as {username} to do that!')
        return redirect('/login')

@app.route('/users/<username>/feedback/add')
def show_feedback_form(username):
    user = User.query.filter_by(username=username).first()
    logged_in_username = session.get('user')
    if logged_in_username == user.username:
        form = FeedbackSubmissionForm()
        return render_template('feedback-submission-form.html', form=form, user=user)
    else:
        flash(f'You must be logged in as {username} to do that!')
        return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['POST'])
def process_feedback(username):
    user = User.query.filter_by(username=username).first()
    logged_in_username = session.get('user')
    if logged_in_username == user.username:
        form = FeedbackSubmissionForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            flash(f'{title} added!')
            return redirect(f'/users/{username}')
        else:
            return render_template('feedback-submission-form.html', form=form)
    else:
        flash(f'You must be logged in as {username} to do that!')
        return redirect('/login')        

@app.route('/feedback/<int:feedback_id>/update')
def update_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    user = feedback.user
    logged_in_username = session.get('user')
    if logged_in_username == user.username:
        form = FeedbackSubmissionForm()
        form.title.data = feedback.title
        form.content.data = feedback.content
        return render_template('feedback-edit-form.html', form=form, user=user, feedback=feedback)
    else:
        flash(f'You must be logged in as {user.username} to access that page!')
        return redirect('/login')

@app.route('/feedback/<int:feedback_id>/update', methods=['POST'])
def process_update(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    user = feedback.user
    logged_in_username = session.get('user')
    if logged_in_username == user.username:
        form = FeedbackSubmissionForm()
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            flash(f'{feedback.title} updated!')
            return redirect(f'/users/{user.username}')
        else:
            return render_template('feedback-edit-form.html', form=form, user=user, feedback=feedback)
    else:
        flash(f'You must be logged in as {user.username} to do that!')
        return redirect('/login')

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    user = feedback.user
    logged_in_username = session.get('user')
    if logged_in_username == user.username:
        db.session.delete(feedback)
        db.session.commit()
        flash(f'{feedback.title} deleted!')
        return redirect(f'/users/{user.username}')
    else:
        flash(f'You must be logged in as {user.username} to do that!')
        return redirect('/login')
