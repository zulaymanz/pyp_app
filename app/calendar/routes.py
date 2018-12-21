from flask import render_template, request, Blueprint
from app import app, db
# LOGIN
from flask_login import current_user
# UTILS
from app.calendar.utils import get_cal, date_list, get_revision_dates, string_to_date, NOW, DAYS
# MODELS
from app.models import User, Subject, Grade, Revision, Topic, load_user

calendar = Blueprint('calendar', __name__)

@calendar.route('/calendar/', defaults={'year': NOW.year, 'month': NOW.month})
@calendar.route('/calendar/<int:year>/<int:month>')
def dashboard(month, year):
  # Resets calendar
  cal = get_cal()
  # subjects = db.session.query(Subject).order_by(Subject.subject_name).all()
  query = db.session.query(Revision.topic, Revision.start_date, Revision.notes, Subject.subject_name, Subject.color_id, Grade.grade_name).join(Subject).join(Grade)
  # query = db.session.query(MyTable).filter(MyTable.name==u'john')
  # query = db.session.query(Revision).order_by(Subject.subject_name)
  for q in query:
    _start_date = q.start_date
    _rev_dates = [date for date in get_revision_dates(string_to_date(_start_date))]
    _rev_dates.insert(0, q.topic)
    for d in range(1, len(_rev_dates) - 1):
      if int(_rev_dates[d].split('-')[1]) == int(month):
        if cal[int(_rev_dates[d].split('-')[1]) - 1] is None:
          cal[int(_rev_dates[d].split('-')[1]) - 1] = [
            {_rev_dates[0]: _rev_dates[d], 'color': q.color_id, 'notes': q.notes, 'grade':q.grade_name}]
        else:
          cal[int(_rev_dates[d].split('-')[1]) - 1].append(
            {_rev_dates[0]: _rev_dates[d], 'color': q.color_id, 'notes': q.notes, 'grade':q.grade_name}) 

  today = [NOW.month, NOW.strftime("%d-%m-%Y")]
  ref = [i for i in date_list(month, year)]
  result = ref
  if sum(n is None for n in cal) < 12:
    for i in range(0, len(result)):
      for d in cal[month - 1]:
        if ref[i] == int(list(d.values())[0].split('-')[2]):
          if isinstance(result[i], int):
            result[i] = {list(d.keys())[0]: [list(d.values())[1], list(d.values())[2], list(d.values())[3]]}
          else:
            result[i].update({list(d.keys())[0]: [list(d.values())[1], list(d.values())[2], list(d.values())[3]]})
    
  return render_template('calendar.htm.j2', calendar=ref, res=cal, days=DAYS, today=today, curr_month=month, curr_year=year)