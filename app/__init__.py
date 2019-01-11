from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import calendar as cl

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'users.login'

from app.main.routes import main
from app.school.routes import school
from app.users.routes import users
from app.calendar.routes import calendar
from app.papers.routes import pyp
from app.rev_iter.routes import rev

app.register_blueprint(main)
app.register_blueprint(school)
app.register_blueprint(users)
app.register_blueprint(calendar)
app.register_blueprint(pyp)
app.register_blueprint(rev)

@app.template_filter('str_month')
def reverse_filter(s):
    return cl.month_name[s]