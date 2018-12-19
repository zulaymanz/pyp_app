from app import app, db, login
from flask import render_template, request, url_for, redirect, flash, current_app, jsonify, Blueprint
from werkzeug.urls import url_parse

# LOGIN
from flask_login import current_user, login_user, login_required, logout_user
# MODELS
from app.models import User, Subject, Grade, Revision, Topic, load_user
# FORMS
from app.users.forms import LoginForm, RegistrationForm

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
      return redirect(url_for('main.index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      message = 'Invalid username or password'
      flash(message, 'warning')
      return redirect(url_for('users.login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('main.index')
    return redirect(next_page)

  return render_template('auth/login.htm.j2', title='Sign In', form=form)

@users.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('main.index'))

@users.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data, urole='STUDENT')
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    message = 'Congratulations, you are now a registered user!'
    flash(message, 'success')
    return redirect(url_for('users.login'))
  return render_template('auth/register.htm.j2', title='Register', form=form)
