from app import db
from flask import render_template, request, Blueprint, flash, redirect, url_for
from sqlalchemy import update
# LOGIN
from flask_login import current_user
# MODELS
from app.models import Calendar, load_user
# UTILS
from app.calendar.utils import REV_DATES

rev = Blueprint('rev', __name__)
@rev.route('/school/iter', methods = ['POST', 'GET'])
# @login_required
def rev_iter():
  r = REV_DATES
  if request.method == 'POST':
    inputs = ["iter-"+str(x) for x in range(1,len(r)+1)]
    iters = [request.form[inp] for inp in inputs]
    i = '-'.join(iters)
    # update(Calendar).where(Calendar.id==1).values(iteration=i)
    db.session.query(Calendar).filter_by(id=1).update({"iteration":(i)})
    try:
      db.session.commit()
      success = 'Iteration updated!'
      flash(success, 'success')
    except:
      error = 'Error insert operation.'
      flash(error, 'warning')
    finally:
      return redirect(url_for('rev.rev_iter'))
    flash(i, 'success')
  return render_template('iter/index.html', r=r)