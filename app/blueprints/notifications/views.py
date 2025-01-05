import flask_login

from app.blueprints.notifications import notifications as notifications_bp
from app.blueprints.notifications.notifications_bp import NotificationsBp


@notifications_bp.route('/register_token/', methods=['GET'])
@flask_login.login_required
def register_token():
    return NotificationsBp().register_token()


@notifications_bp.route('/send/', methods=['GET'])
@flask_login.login_required
def send():
    return NotificationsBp().send()


@notifications_bp.route('/fcm/', methods=['GET'])
@flask_login.login_required
def fcm():
    return NotificationsBp().fcm_view()


@notifications_bp.route('/table/', methods=['GET'])
@flask_login.login_required
def table():
    return NotificationsBp().table()
