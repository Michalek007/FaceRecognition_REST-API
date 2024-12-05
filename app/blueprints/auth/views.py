import flask_login

from app.blueprints.auth import auth
from app.blueprints.auth.auth_bp import AuthBp
from app.blueprints import login_manager


@login_manager.user_loader
def user_loader(login):
    return AuthBp().user_loader(login=login)


@login_manager.request_loader
def request_loader(request):
    return AuthBp().request_loader(request=request)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return AuthBp().unauthorized_handler()


@auth.route('/')
def base():
    return AuthBp().base()


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """ Allows to log into service.
        Input args: login, password.
        If logging was successful you will be redirected to url:
        GET method -> /protected/
        POST method -> /logged_in/
    """
    return AuthBp().login()


@auth.route('/logged_in/')
@flask_login.login_required
def logged_in():
    return AuthBp().logged_in()
