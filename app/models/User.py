from flask_login import UserMixin
from app import db
import hashlib
from app import db, login_manager

class User(UserMixin,db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(128), index=False)
    last_name = db.Column(db.String(128), index=False)
    address = db.Column(db.String(128), index=False)
    doornumber = db.Column(db.String(32), index=False)
    apartment = db.Column(db.String(32), index=False)
    email = db.Column(db.String(128), index=True, unique=True)
    phonenumber = db.Column(db.String(60), index=False, unique=False)
    cellphonenumber = db.Column(db.String(60), index=False, unique=False)
    password_hash = db.Column(db.String(128))
    visible = db.Column(db.Boolean)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        """hashlib.md5(password).hexdigest()"""
        password = password + "20eTagteN26"
        return hashlib.md5(password.encode("utf")).hexdigest() == self.password_hash

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('User', backref='users',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
