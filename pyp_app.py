from app import app, db
from app.models import User, Subject, Revision, Grade

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'Subject': Subject, 'Revision': Revision, 'Grade': Grade}