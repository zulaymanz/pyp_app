from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

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

app.register_blueprint(main)
app.register_blueprint(school)
app.register_blueprint(users)
app.register_blueprint(calendar)