        add_minutes = int(form.minutesf.data)
        add_hours = int(form.hoursf.data)
        total_time.hours += add_hours
        total_time.minutes += add_minutes
        db.session.add(total_time)
        db.session.commit()

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True)
    todos = db.relationship('Todo', backref='date_day', lazy='dynamic')
    overall = db.Column(db.String(140))
    conclusion = db.Column(db.String(140))
    comments =  db.relationship('comment_day', backref='container', lazy='dynamic')

    def __repr__(self):
        return '<Activity {}>'.format(self.timestamp)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    progress = db.Column(db.String(140))
    ifdone = db.column(db.Boolean)
    hours = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    day = db.Column(db.Integer, db.ForeignKey('day.id'))

    def __repr__(self):
        return '<Activity {}>'.format(self.body)



class Done(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    day = db.Column(db.Integer, db.ForeignKey('day.id'))

from app import db
from app.models import *
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