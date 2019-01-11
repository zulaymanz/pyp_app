import calendar
import datetime

from sqlalchemy.orm import Session, load_only
from app.models import Calendar
from app import db

from datetime import timedelta

dtdt = datetime.datetime

# Constant
NOW = datetime.datetime.now()
# Revision iterations
# [int(x.strip()) for x in iter_dates.split('-')]
def get_iter():
  i = db.session.query(Calendar).options(load_only("iteration")).all()
  return [int(x.strip()) for x in i[0].iteration.split('-')]

def get_dateFormats():
  d = db.session.query(Calendar).options(load_only("date_format")).all()
  return d[0].date_format 

# [1, 7, 30, 183]
REV_DATES = get_iter()
# REV_DATES = [1, 7, 30, 183]
# '%Y-%m-%d'
DATE_FORMAT = get_dateFormats()

dl = calendar.TextCalendar(calendar.SUNDAY)
"""
List of days in the month 1,2,3...30
0 for days of the next month
"""
DATE_LIST = dl.itermonthdays(2018, NOW.month)
DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_cal():
  return [None] * 12

def date_list(month, year):
  return dl.itermonthdays(year, month)


def get_days_from_month(month):
  return dl.itermonthdays(2018, month)


def check_date(date, month, doc, cal):
  for d in cal[month - 1]:
    if date == int(list(d.values())[0].split('-')[2]):
      if doc[date - 1] is None or isinstance(doc[date - 1], int):
        doc[date - 1] = [list(d.keys())[0]]
      else:
        doc[date - 1].append(list(d.keys())[0])
    elif doc[date - 1] is None:
      doc[date - 1] = date
  return doc


# get an array of revision dates from a start date
def get_revision_dates(start_date):
  i = start_date
  result = []
  for r in REV_DATES:
    i = i + timedelta(days=r)
    result.append(format_date(i))
  return result


# get date to desired format
def format_date(date):
  return dtdt.strftime(date, DATE_FORMAT)


# get date in string
def string_to_date(date):
  return dtdt.strptime(date, DATE_FORMAT)