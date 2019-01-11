from app import db, login
from datetime import datetime
from flask_login import UserMixin

# security
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  urole = db.Column(db.String(80))
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def get_urole(self):
    return self.urole

  def __repr__(self):
    return '<User {}>'.format(self.username)

class Subject(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  subject_name = db.Column(db.String(64), index=True)
  color_id = db.Column(db.String(64), index=True)

  def __repr__(self):
    return '<Subject {}>'.format(self.subject_name)

class Grade(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  grade_name = db.Column(db.String(64), index=True)

  def __repr__(self):
    return '<Grade {}>'.format(self.grade_name)

class Topic(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  topic_name = db.Column(db.String(64), index=True)
  subject = db.Column(db.Integer, db.ForeignKey('subject.id'))

  def __repr__(self):
    return '<Topic {}>'.format(self.topic_name)

class Revision(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  start_date = db.Column(db.String(64), index=True)
  topic = db.Column(db.String(64), index=True)
  subject = db.Column(db.Integer, db.ForeignKey('subject.id'))
  notes = db.Column(db.String(140))
  grade = db.Column(db.Integer, db.ForeignKey('grade.id'))
  
  def __repr__(self):
    return '<Revision {}>'.format(self.id)


class Calendar(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  iteration = db.Column(db.String(64), index=True)
  date_format = db.Column(db.String(64), index=True)

  def __repr__(self):
    return '<Calendar {}>'.format(self.id)