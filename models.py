"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):

    __tablename__="users"

    def __repr__(self):
        return f'<Username: {self.username}, password: {self.password}, email: {self.email}, first_name: {self.first_name}, last_name: {self.last_name}'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback',backref='users',cascade="all, delete-orphan")

    # solution said cascade="all,delete"
    # use self.password to pull from main user model

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(password)
        decoded_hash = hashed.decode('utf8')

        return cls(username=username, password=decoded_hash,email=email,first_name=first_name,last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):

    def __repr__(self):
        s = self
        return f"Id: {s.id}, Title: {s.title}, Content: {s.content}, Username: {s.username}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    username = db.Column(db.String(20),db.ForeignKey('users.username'),nullable=False)