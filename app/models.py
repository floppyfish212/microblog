from app import db, login
from hashlib import md5
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

# db.Model is a base model from Flask-SQLAlchemy
class User(UserMixin, db.Model):

	# UserMixin adds
	#    is_authenticated: property that is True if the user has valid credentials or False otherwise
	#    is_active:        property that is True if the user account is active or False otherwise
	#    is_anonymous:     property that is False for regular users or True for a special, anon user 
	#    is_id():          method that returns a unique identifier for the user as a string

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):           # note: self is used internally to the class
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):         # note: self is used internally to the class
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?s={}'.format(digest, size) 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
    	return '<Post {}>'.format(self.body)

