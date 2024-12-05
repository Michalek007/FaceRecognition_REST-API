from flask import Blueprint

env_metrics = Blueprint('env_metrics',
                        __name__,
                        # url_prefix='/env_metrics',
                        template_folder='templates')

from app.blueprints.env_metrics import views
