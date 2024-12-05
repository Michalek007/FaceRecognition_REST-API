import flask_login

from app.blueprints.user import user
from app.blueprints.user.user_bp import UserBp


@user.route('/register/', methods=['GET', 'POST'])
def register():
    """ Allows to register new user.
        Input args: login, password, repeat_password.
    """
    return UserBp().register()


@user.route('/logout/', methods=['GET'])
@flask_login.login_required
def logout():
    """ Allows to log out from application. """
    return UserBp().logout()


@user.route('/protected/', methods=['GET'])
@flask_login.login_required
def protected():
    """ Returns currently logged users in service.
        Output keys: logged_user.
    """
    return UserBp().protected()


@user.route('/users/<int:user_id>/', methods=['GET'])
@user.route('/users/', methods=['GET'])
def users(user_id: int = None):
    """ Returns user with given id or if not specified list of all users from database.
        Input args: /id/.
        Output keys: Users/User {id, pw_hash, username}.
    """
    return UserBp().users(user_id=user_id)


@user.route('/users_table/', methods=['GET'])
def users_table():
    return UserBp().users_table()
