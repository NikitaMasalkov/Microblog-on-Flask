from app import login
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='comment_author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    todos = db.relationship('Todo', backref='activity_day', lazy='dynamic')
    overall = db.Column(db.String(140))
    conclusion = db.Column(db.String(140))
    comments =  db.relationship('Comment', backref='container', lazy='dynamic')

    def __repr__(self):
        return '<Activity {}>'.format(self.timestamp)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    progress = db.Column(db.String(140))
    ifdone = db.column(db.Boolean)
    hours = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))

    def __repr__(self):
        return '<Activity {}>'.format(self.body)



class Done(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    day = db.Column(db.Integer, db.ForeignKey('day.id'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Integer)
    minutes = db.Column(db.Integer)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))