from flask import render_template, request, Blueprint
from app import app, db
# LOGIN
from flask_login import current_user
# UTILS
from app.calendar.utils import get_cal
# MODELS
from app.models import User, Subject, Grade, Revision, Topic, load_user

calendar = Blueprint('calendar', __name__)

# @calendar.route('/calendar/', defaults={'year': NOW.year, 'month': NOW.month})
@calendar.route('/calendar/<int:year>/<int:month>')
def calnedar(month, year):
  # Resets calendar
  cal = get_cal()
  subjects = db.session.query(Subject).order_by(Subject.subject_name).all()
