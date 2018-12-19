from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateField
from app.models import User

class NewGradeForm(FlaskForm):
  name = StringField('Grade name', validators=[DataRequired()], render_kw={"placeholder": "Senior/Junior/etc."})
  submit = SubmitField("Submit")

class NewSubjectForm(FlaskForm):
  subject = StringField('Subject name', validators=[DataRequired()])
  submit = SubmitField("Submit")

class NewTopicForm(FlaskForm):
  topic = StringField('Topic name', validators=[DataRequired()])
  submit = SubmitField("Submit")

class NewRevisionForm(FlaskForm):
  start_date = DateField('Date', validators=[DataRequired()])
  notes = TextAreaField('Notes' )
  submit = SubmitField("Submit")