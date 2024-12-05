from flask import Blueprint

auth = Blueprint('auth',
                 __name__,
                 # url_prefix='/auth',
                 template_folder='templates')

from app.blueprints.auth import views
