from flask import Blueprint

members = Blueprint('members',
                    __name__,
                    url_prefix='/members',
                    template_folder='templates')

from app.blueprints.members import views
