from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    """Form for registering new users"""

    username = StringField('Username', validators=[InputRequired(message='Please enter a username'), Length(max=20, message='Username must be 20 character or less')])
    password = PasswordField('Password', validators=[InputRequired(message='Please enter a password'), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm password', validators=[InputRequired(), Length(max=50, message='Email must be 50 characters or less')])
    email = EmailField('Email', validators=[InputRequired(message='Please enter an email address')])
    first_name = StringField('First name', validators=[InputRequired(message='Please enter your first name'), Length(max=30, message='First name must be 30 characters or less')])
    last_name = StringField('Last name', validators=[InputRequired(message='Please enter your last name'), Length(max=30, message='Last name must be 30 characters or less')])

class LoginForm(FlaskForm):
    """Form for logging in existing users"""

    username = StringField('Username', validators=[InputRequired(message='Please enter a username'), Length(max=20, message='Username must be 20 character or less')])
    password = PasswordField('Password', validators=[InputRequired(message='Please enter a password')])
