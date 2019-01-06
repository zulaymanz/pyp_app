import os
from app import db
from flask import render_template, request, Blueprint, redirect, url_for, flash
from werkzeug.utils import secure_filename
# LOGIN
from flask_login import current_user
# FORMS
from app.papers.forms import UploadForm
# MODELS
from app.models import User, Subject, Grade, Revision, Topic, load_user

from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

# Cloud.config.update = ({
  # 'cloud_name':os.environ.get('CLOUDINARY_CLOUD_NAME'),
  # 'api_key': os.environ.get('CLOUDINARY_API_KEY'),
  # 'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
  # 'cloud_name':os.environ.get('zulaymanz'),
  # 'api_key': os.environ.get('615294135897313'),
  # 'api_secret': os.environ.get('gM8Jz7Tv4E0ebz0d7pAQTBhUHs8')
# })

pyp = Blueprint('pyp', __name__)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

DEFAULT_TAG = "python_sample_basic"

def dump_response(response):
  print("Upload response:")
  for key in sorted(response.keys()):
    print("  %s: %s" % (key, response[key]))

@pyp.route('/school/pyp', methods=['GET', 'POST'])
def dashboard():
  # QUERIES
  topics = db.session.query(Topic).order_by(Topic.topic_name).all()

  form = UploadForm()
  if form.validate_on_submit():
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      # filename = secure_filename(file.filename)
      # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      response = upload(file, tags=DEFAULT_TAG)
      dump_response(response)
      url = cloudinary_url(
        response['public_id'],
        format=response['format'],
        width=200,
        height=150,
        crop="fill"
      )
      # pipeshelf = Cloud.uploader.upload(filename)
      return redirect(url_for('pyp.dashboard'))
    return redirect(url_for('pyp.dashboard'))
  
  return render_template('pyp/new.html', form=form, topics=topics)