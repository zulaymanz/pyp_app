from app import app, db, login
from sqlalchemy.orm import Session, load_only
from flask import render_template, request, url_for, redirect, flash, current_app, jsonify, Blueprint
# LOGIN
from flask_login import current_user
# FORMS
from app.school.forms import NewGradeForm, NewSubjectForm, NewRevisionForm, NewTopicForm
# UTILS
from app.users.utils import login_required
# MODELS
from app.models import User, Subject, Grade, Revision, Topic, load_user

school = Blueprint('school', __name__)

formhelpers = '_formhelpers.html'

@school.route('/school/', methods=['GET', 'POST'])
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
        return redirect(url_for('school.restricted_view_for_school'))
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
        error = 'Error insert operation.'
        flash(error, 'danger')
      finally:
        return redirect(url_for('school.restricted_view_for_school'))

  if grade_form.validate_on_submit() and grade_form.submit.data:
    grade_name = grade_form.name.data
    grade = Grade(grade_name=grade_name)
    db.session.add(grade)
    try:
      db.session.commit() 
      success = 'New Grade added!'
      flash(success, 'success')
    except:
      error = 'Error insert operation.'
      flash(error, 'danger')
    finally:
      return redirect(url_for('school.restricted_view_for_school'))

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
      error = 'Error insert operation.'
      flash(error, 'danger')
    finally:
      return redirect(url_for('school.restricted_view_for_school'))

  return render_template('school/dashboard.htm.j2',
                          gform=grade_form, sform=subject_form, rform=revision_form, tform=topic_form,
                          fh=formhelpers, grades=grades, subjects=subjects, topics=topics, revisions=revisions)

@school.route('/autocomplete', methods=['GET'])
def autocomplete():
  search = request.args.get('q')
  query = db.session.query(Topic.topic_name, Subject.subject_name).join(Subject).filter(Topic.topic_name.like('%' + str(search) + '%'))
  results = [{mv[1]:mv[0]} for mv in query.all()]
  return jsonify(matching_results=results)
