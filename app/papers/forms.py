from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from app.models import User

class UploadForm(FlaskForm):
    file = FileField()