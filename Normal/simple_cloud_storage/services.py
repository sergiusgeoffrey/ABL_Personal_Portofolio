import os
import uuid
import datetime
from django import apps
from django.conf import settings
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


#upload file
def UploadFile(file):
    filename = secure_filename(file.filename)
    file.save(os.path.join(apps.config['UPLOAD_FOLDER'], filename))
    return filename
    
#download file
def DownloadFile(filename):
    return os.path.join(apps.config['UPLOAD_FOLDER'], filename)