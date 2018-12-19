from flask import render_template, request, url_for, redirect, flash, current_app, jsonify
from flask_login import current_user
from functools import wraps

def login_required(role="ANY"):
  def wrapper(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
      if not current_user.is_authenticated:
         return current_app.login_manager.unauthorized()
      # u = current_app.login_manager.reload_user()
      urole = current_user.urole
      if ( (urole != role) and (role != "ANY")):
          return current_app.login_manager.unauthorized()      
      return fn(*args, **kwargs)
    return decorated_view
  return wrapper