from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = 'Users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    feedback = db.relationship('Feedback', cascade='all, delete-orphan')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        pw_hash = bcrypt.generate_password_hash(password)
        pw_hash_utf8 = pw_hash.decode('utf8')
        return cls(username=username, password=pw_hash_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    def get_full_name(self):
        """Return full name for a user instance"""
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'<User username: {self.username}, email: {self.email}, first_name: {self.first_name}, last_name: {self.last_name}>'

class Feedback(db.Model):
    """Feedback"""

    __tablename__ = 'Feedback'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('Users.username'))
    user = db.relationship('User')

    def __repr__(self):
        return f'<Feedback id: {self.id}, title: {self.title}, content: {self.content}, username: {self.username}>'
