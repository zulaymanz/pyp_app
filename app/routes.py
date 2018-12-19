from flask import render_template, request, url_for, redirect, flash, current_app, jsonify
from app import app, db, login
from functools import wraps
from werkzeug.urls import url_parse
from sqlalchemy.orm import Session, load_only
import sys

session = Session()

# FORMS
from app.forms import LoginForm, RegistrationForm, NewGradeForm, NewSubjectForm, NewRevisionForm, NewTopicForm
# LOGIN
from flask_login import current_user, login_user, login_required, logout_user
# MODELS
from app.models import User, Subject, Grade, Revision, Topic, load_user

formhelpers = '_formhelpers.html'

@app.route('/')
@app.route('/index')
# @login_required
def index():
  posts = [
    {
      'author': {'username': 'John'},
      'body': 'Beautiful day in Portland!'
    },
    {
      'author': {'username': 'Susan'},
      'body': 'The Avengers movie was so cool!'
    }
  ]
  icon = "teacher.svg"
  if current_user.is_authenticated:
    if current_user.urole == 'STUDENT':
      icon = 'student.svg'
  return render_template('index.htm.j2', icon=icon, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
      return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      message = 'Invalid username or password'
      flash(message, 'warning')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)

  return render_template('auth/login.htm.j2', title='Sign In', form=form)

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
    user = User(username=form.username.data, email=form.email.data, urole='STUDENT')
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    message = 'Congratulations, you are now a registered user!'
    flash(message, 'success')
    return redirect(url_for('login'))
  return render_template('auth/register.htm.j2', title='Register', form=form)

def login_required(role="ANY"):
  def wrapper(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
      if not current_user.is_authenticated:
         return current_app.login_manager.unauthorized()
      u = current_app.login_manager.reload_user()
      urole = current_user.urole
      if ( (urole != role) and (role != "ANY")):
          return current_app.login_manager.unauthorized()      
      return fn(*args, **kwargs)
    return decorated_view
  return wrapper

def get_cal():
  return [None] * 12

@app.route('/calendar/', defaults={'year': NOW.year, 'month': NOW.month})
@app.route('/calendar/<int:year>/<int:month>')
def calndr(month, year):
  # Resets calendar
  cal = get_cal()
  subjects = db.session.query(Subject).order_by(Subject.subject_name).all()


@app.route('/school/', methods=['GET', 'POST'])
@login_required(role="TEACHER")
def restricted_view_for_school():
  # QUERIES
  grades = db.session.query(Grade).order_by(Grade.grade_name).all()
  subjects = db.session.query(Subject).order_by(Subject.subject_name).all()
  revisions = db.session.query(Revision).order_by(Revision.timestamp).all()
  topics = db.session.query(Topic).order_by(Topic.topic_name).all()
  colors = db.session.query(Subject).options(load_only("color_id")).all()
  # FORMS
  grade_form = NewGradeForm(prefix='grade_form')
  subject_form = NewSubjectForm(prefix='subject_form')
  revision_form = NewRevisionForm(prefix='revision_form')
  topic_form = NewTopicForm(prefix='topic_form')

  error = None

  if revision_form.validate_on_submit() and revision_form.submit.data:
    grade = request.form['grade']
    subject = db.session.query(Subject).filter_by(subject_name=request.form['subject']).first()
    topic = request.form['topic']
    start_date = revision_form.start_date.data
    notes = revision_form.notes.data

    if None not in (grade, subject, topic):
      revision = Revision(start_date=str(start_date), topic=topic, subject=subject.id, notes=notes, grade=grade)
      db.session.add(revision)
      try:
        db.session.commit() 
        success = 'New Revision created!'
        flash(success, 'success')
      except:
        error = 'Error insert operation.'
        flash(error, 'warning')
      finally:
        return redirect(url_for('restricted_view_for_school'))
    else:
      error = 'Something went wrong.'
      flash(error, 'warning')

  if subject_form.validate_on_submit() and subject_form.submit.data:
    color_id = request.form['color_id']
    subject = subject_form.subject.data

    if color_id in [c.color_id for c in colors]:
      error = 'Sorry color already in use. Pick another one.'

    if error is not None:
      flash(error, 'danger')
    else:
      subject = Subject(subject_name=subject, color_id=color_id)
      db.session.add(subject)
      try:
        db.session.commit() 
        success = 'Subject added!'
        flash(success, 'success')
      except:
        session.rollback()
        raise
        error = 'Error insert operation.'
        flash(error, 'danger')
      finally:
        return redirect(url_for('restricted_view_for_school'))

  if grade_form.validate_on_submit() and grade_form.submit.data:
    grade_name = grade_form.name.data
    grade = Grade(grade_name=grade_name)
    db.session.add(grade)
    try:
      db.session.commit() 
      success = 'New Grade added!'
      flash(success, 'success')
    except:
      session.rollback()
      raise
      error = 'Error insert operation.'
      flash(error, 'danger')
    finally:
      return redirect(url_for('restricted_view_for_school'))

  if topic_form.validate_on_submit() and topic_form.submit.data:
    topic_name = topic_form.topic.data
    subject = request.form['subject']

    topic = Topic(topic_name=topic_name, subject=subject)
    db.session.add(topic)
    try:
      db.session.commit() 
      success = 'New Topic added!'
      flash(success, 'success')
    except:
      db.session.rollback()
      raise
      error = 'Error insert operation.'
      flash(error, 'danger')
    finally:
      return redirect(url_for('restricted_view_for_school'))

  return render_template('school/dashboard.htm.j2',
                          gform=grade_form, sform=subject_form, rform=revision_form, tform=topic_form,
                          fh=formhelpers, grades=grades, subjects=subjects, topics=topics, revisions=revisions)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
  search = request.args.get('q')
  query = db.session.query(Topic.topic_name, Subject.subject_name).join(Subject).filter(Topic.topic_name.like('%' + str(search) + '%'))
  results = [{mv[1]:mv[0]} for mv in query.all()]
  return jsonify(matching_results=results)

@app.route('/about')
def about():
  return render_template('about.htm.j2')