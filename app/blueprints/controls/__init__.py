from flask import Blueprint

controls = Blueprint('controls',
                     __name__,
                     # url_prefix='/controls',
                     template_folder='templates')

from app.blueprints.controls import views
