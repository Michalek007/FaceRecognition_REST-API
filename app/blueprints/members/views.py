import flask_login

from app.blueprints.members import members as members_bp
from app.blueprints.members.members_bp import MembersBp


@members_bp.route('/get/<int:member_id>/', methods=['GET'])
@members_bp.route('/get/', methods=['GET'])
@flask_login.login_required
def get(member_id: int = None):
    return MembersBp().get(member_id=member_id)


@members_bp.route('/add/', methods=['POST'])
@flask_login.login_required
def add():
    return MembersBp().add()


@members_bp.route('/delete/', methods=['DELETE'])
@members_bp.route('/delete/<int:member_id>/', methods=['DELETE'])
@flask_login.login_required
def delete(member_id: int = None):
    return MembersBp().delete(member_id=member_id)


@members_bp.route('/update/<int:member_id>/', methods=['PUT'])
@flask_login.login_required
def update(member_id: int = None):
    return MembersBp().update(member_id=member_id)


@members_bp.route('/upload_image/', methods=['POST'])
@flask_login.login_required
def upload_image():
    return MembersBp().upload_image()


@members_bp.route('/new/', methods=['POST'])
@flask_login.login_required
def new():
    return MembersBp().new()


@members_bp.route('/table/', methods=['GET'])
@flask_login.login_required
def table():
    return MembersBp().table()


@members_bp.route('/upload/', methods=['GET'])
@flask_login.login_required
def upload():
    return MembersBp().upload()
