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


@notifications_bp.route('/get_all/', methods=['GET'])
@flask_login.login_required
def get_all():
    return NotificationsBp().get_all()


@notifications_bp.route('/delete_all/', methods=['GET'])
@flask_login.login_required
def delete_all():
    return NotificationsBp().delete_all()


@notifications_bp.route('/set/', methods=['POST'])
@flask_login.login_required
def set():
    return NotificationsBp().set()


@notifications_bp.route('/get/', methods=['GET'])
@flask_login.login_required
def get():
    return NotificationsBp().get()


@notifications_bp.route('/fcm/', methods=['GET'])
@flask_login.login_required
def fcm():
    return NotificationsBp().fcm_view()


@notifications_bp.route('/table/', methods=['GET'])
@flask_login.login_required
def table():
    return NotificationsBp().table()
