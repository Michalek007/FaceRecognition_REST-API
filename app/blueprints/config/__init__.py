from flask import Blueprint

config = Blueprint('config',
                   __name__,
                   # url_prefix='/config',
                   template_folder='templates')

from app.blueprints.config import views
