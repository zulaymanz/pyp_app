from flask import render_template, request, Blueprint
# LOGIN
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
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


@main.route('/about')
def about():
  return render_template('about.htm.j2')