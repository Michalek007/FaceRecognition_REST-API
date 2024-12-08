from flask import Blueprint

face_recognition = Blueprint('face_recognition',
                             __name__,
                             url_prefix='/face',
                             template_folder='templates')

from app.blueprints.face_recognition import views
