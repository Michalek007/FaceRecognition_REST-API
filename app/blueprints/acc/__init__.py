from flask import Blueprint

acc = Blueprint('acc',
                __name__,
                # url_prefix='/acc',
                template_folder='templates')

from app.blueprints.acc import views
