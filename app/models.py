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
    overall = db.Column(db.String(140))
    conclusion = db.Column(db.String(140))
    activities = db.relationship('Activity', backref='date', lazy='dynamic')
    comments = db.relationship('Comment', backref='comment_date', lazy='dynamic')
    task = db.Column(db.String(140))
    month_str = db.Column(db.String(140))
    total_minutes = db.Column(db.Integer)
    total_hours = db.Column(db.Integer)

    def __repr__(self):
        return '<Day {}>'.format(self.timestamp)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    hours = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    prehours = db.Column(db.Integer)
    preminutes = db.Column(db.Integer)
    preminutes_str = db.Column(db.String(140))
    completion = db.Column(db.Integer)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    planned_progress = db.Column(db.String(50))
    made_progress = db.Column(db.String(50))





    def __repr__(self):
        return '<Activity {}>'.format(self.name)



class Done(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    day = db.Column(db.Integer, db.ForeignKey('day.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.body)


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