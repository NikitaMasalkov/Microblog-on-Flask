from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from app.models import User, Post, Time, Comment, Day, Activity
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, ReusableForm, EditProfileForm, TimeForm, DayCreationForm, ActivityCreationForm
from datetime import datetime
from datetime import *
from app.time_calculations import total_time_spend, overall_time


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts, )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = ReusableForm(request.form)
    posts = Post.query.all()
    comments = Comment.query.all()
    if form.validate():
        p = Post(body = form.post_text.data, user_id = current_user.id)
        db.session.add(p)
        db.session.commit()
        flash('Congratulations, you have created post!')
        return redirect(url_for('post'))

    return render_template('post.html', title='Post', form = form, posts = posts, comments = comments)

@app.route('/new_day', methods=['GET', 'POST'])
def new_day():
    days = Day.query.all()
    form = DayCreationForm(request.form)

    if form.validate():
        a = Day(task = form.task.data)
        db.session.add(a)
        db.session.commit()
        day = Day.query.order_by(Day.id.desc()).first()
        date_ = day.timestamp
        new_month = str(form.day.data)
        new_day = str(form.month.data)
        date_ = date_.strptime(new_month + "-" + new_day, "%m-%d")
        day.timestamp = date_
        day.month_str = date_.strftime('%B')
        db.session.add(day)
        db.session.commit()

        return redirect(url_for('activity_manager'))
    return render_template('new_day.html', form = form, days = days)



@app.route('/delete', methods=['GET', 'POST'])
def delete():

    posts = Post.query.all()
    for po in posts:
      db.session.delete(po)
    db.session.commit()

    return render_template('delete.html', title='Delete', posts=posts)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/day_edit/<the_day>',methods=['GET', 'POST'])
def day_edit(the_day):
  day = Day.query.get(the_day)
  form = DayCreationForm(request.form)
  if form.validate():
      day.task = form.task.data
      date_ = day.timestamp
      new_day = str(form.day.data)
      new_month = str(form.month.data)
      date_ = date_.strptime(new_month + "-" + new_day, "%m-%d")
      day.timestamp = date_
      day.month_str = date_.strftime('%B')
      db.session.add(day)
      db.session.commit()
      flash('Your changes have been saved.')
      return redirect(url_for('activity_manager'))
  elif request.method == 'GET':
      form.task.data = day.task
      form.day.data = day.timestamp.day
      form.month.data = day.timestamp.month
  return render_template('day_edit.html', title='Edit day',
                         form=form, day = day)


@app.route('/edit_activities/<activity_day>',methods=['GET', 'POST'])
def edit_activities(activity_day):
    day = Day.query.get(activity_day)
    activities = day.activities
    form = ActivityCreationForm(request.form)
    if form.validate():
        new_activity = Activity(name = form.name.data, prehours = form.hours.data, preminutes = form.minutes.data,
                                completion = form.done.data, planned_progress = form.progress.data, day_id = day.id,
                                made_progress = " ", hours = 0, minutes = 0)
        db.session.add(new_activity)
        db.session.commit()
        return redirect(url_for('activity_manager'))
    return render_template('edit_activities.html', activities = activities, day=day, form = form)


@app.route('/approve_activity/<the_activity>',methods=['GET', 'POST'])
def approve_activity(the_activity):
    activity = Activity.query.get(the_activity)
    form = ActivityCreationForm(request.form)
    if request.method == "POST":
        activity.made_progress = form.progress.data
        activity.minutes = form.minutes.data
        activity.hours = form.hours.data
        activity.completion = form.done.data
        db.session.add(activity)
        db.session.commit()
        return redirect(url_for('activity_manager'))

    elif request.method == 'GET':

      if activity.made_progress != " ":
        form.progress.data = activity.made_progress
    form.minutes.data = activity.minutes
    form.hours.data = activity.hours
    return render_template('approve_activity.html', title='Edit day', form = form, activity = activity)


@app.route('/edit_activity/<the_activity>',methods=['GET', 'POST'])
def edit_activity(the_activity):
    activity = Activity.query.get(the_activity)
    form = ActivityCreationForm(request.form)
    refresher = activity.day_id
    if form.validate():
        activity.name = form.name.data
        activity.prehours = form.hours.data
        activity.preminutes = form.minutes.data
        activity.planned_progress = form.progress.data
        db.session.add(activity)
        db.session.commit()
        return redirect(url_for('edit_activities', activity_day = refresher))


    elif request.method == 'GET':
        form.name.data = activity.name
        form.minutes.data =  activity.preminutes
        form.hours.data = activity.prehours
        form.progress.data = activity.planned_progress

    return render_template('edit_activity.html', form = form, activity = activity)


@app.route('/day_delete/<the_day>', methods=['GET', 'POST'])
def day_delete(the_day):
    day = Day.query.get(the_day)
    db.session.delete(day)
    db.session.commit()
    return render_template('delete_day.html')

@app.route('/activity_delete/<the_activity>', methods=['GET', 'POST'])
def activity_delete(the_activity):
    activity = Activity.query.get(the_activity)
    quiter = activity.day_id
    db.session.delete(activity)
    db.session.commit()
    return render_template('delete_activity.html', quiter = quiter)




@app.route ('/delete_activities')
def delete_activities():
    activities = Time.query.all()
    for ac in activities:
        db.session.delete(ac)
    db.session.commit()
    return render_template ('delete_activities.html')


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    form = TimeForm()
    now = datetime.now()
    total_time = Time.query.get(1)
    today = str(now.day) + " " + str(now.month) + " " + str(now.year)
    if total_time is None:
        a = False
        minutes = 0
        hours = 0
        if request.method == 'POST':
          new_entry = Time(hours = 0 , minutes = 0)
          add_minutes = int(form.minutesf.data)
          add_hours = int(form.hoursf.data)
          if add_minutes > 59:
              bonus_hours, add_minutes = divmod(add_minutes, 60)
              add_hours += bonus_hours

          new_entry.hours += add_hours
          new_entry.minutes += add_minutes
          db.session.add(new_entry)
          db.session.commit()
          flash('Time began tracking')
          return redirect(url_for('calculator'))

    else:
        a = True
        minutes = total_time.minutes
        hours = total_time.hours
        if request.method == 'POST':
          add_minutes = int(form.minutesf.data)
          add_hours = int(form.hoursf.data)
          hours += add_hours
          minutes += add_minutes
          if minutes > 59:
              b_hours, minutes = divmod(minutes, 60)
              hours += b_hours
          total_time.hours = hours
          total_time.minutes = minutes
          db.session.add(total_time)
          db.session.commit()
          flash('Activity has been added')
          return redirect(url_for('calculator'))

    return render_template('calculation.html', minutes = minutes, hours=hours, a = a, form = form, today = today)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)




@app.route('/activity_manager', methods=['GET', 'POST'])
def activity_manager():
    days = Day.query.all()

    for day in days:
        day = total_time_spend(day)
        db.session.add(day)
        db.session.commit()
    for day in days:
        _date = day.timestamp
        month = str(_date.month)
        day_ = str(_date.day)
        _date.strptime(month + "-" + day_, "%m-%d")
        db.session.add(day)
        db.session.commit()

    total_time = Time.query.get(1)
    total_time = overall_time(days, total_time)
    db.session.add(total_time)
    db.session.commit()
    days = Day.query.all()
    posts = Post.query.all()
    total_time = Time.query.get(1)

    return render_template('activity_manager.html', days = days, posts = posts, total_time = total_time)


def date_format(date_):
    month = str(date_.month)
    day_ = str(date_.day)
    date_.strptime(month+"-"+day_, "%m-%d")
    return date_







