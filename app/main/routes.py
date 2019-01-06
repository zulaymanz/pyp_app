from flask import render_template, request, Blueprint
# LOGIN
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
# @login_required
def index():
  # icon = "teacher.svg"
  if current_user.is_authenticated:
    page = 'home.html'
    if current_user.urole == 'STUDENT':
      page = 'student/index.htm.j2'
    elif current_user.urole == 'SCHOOL':
      page = 'student/index.htm.j2'
  return render_template(page)

@main.route('/about')
def about():
  return render_template('about.htm.j2')