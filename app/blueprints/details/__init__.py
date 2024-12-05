from flask import Blueprint

details = Blueprint('details',
                    __name__,
                    # url_prefix='/details',
                    template_folder='templates')

from app.blueprints.details import views
