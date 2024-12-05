import flask_login

from app.blueprints.acc import acc as acc_bp
from app.blueprints.acc.acc_bp import AccBp


@acc_bp.route('/acc/<int:acc_id>/', methods=['GET'])
@acc_bp.route('/acc/', methods=['GET'])
def acc(acc_id: int = None):
    """ Returns acc with given id or if not specified list of all acc from database.
        If given timestamp, returns list of acc with later timestamp.
        Input args: /id/, Timestamp.
        Output keys: output {id, x_axis, y_axis, z_axis}
    """
    return AccBp().acc(acc_id=acc_id)


@acc_bp.route('/add_acc/', methods=['POST'])
def add_acc():
    """ POST method.
        Adds acc to database.
        Input args: X, Y, Z.
    """
    return AccBp().add_acc()


@acc_bp.route('/delete_acc/', methods=['DELETE'])
@acc_bp.route('/delete_acc/<int:acc_id>/', methods=['DELETE'])
def delete_acc(acc_id: int = None):
    """ DELETE method.
        Delete acc with given id or if given timestamp, deletes acc with earlier timestamp.
        Input args: /id/, Timestamp.
    """
    return AccBp().delete_acc(acc_id=acc_id)


@acc_bp.route('/update_acc/<int:acc_id>/', methods=['PUT'])
def update_acc(acc_id: int = None):
    """ PUT method.
        Updates acc with given id.
        Input args: X, Y, Z.
    """
    return AccBp().update_acc(acc_id=acc_id)


@acc_bp.route('/acc_table/', methods=['GET'])
def acc_table():
    return AccBp().acc_table()
