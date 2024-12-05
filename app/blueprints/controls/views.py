import flask_login

from app.blueprints.controls import controls as bp_controls
from app.blueprints.controls.controls_bp import ControlsBp


@bp_controls.route('/get_action/', methods=['GET'])
def get_action():
    """ Returns current action.
        Output keys: action.
    """
    return ControlsBp().get_action()  # + 1


@bp_controls.route('/update_action/<int:value>/', methods=['PUT'])
def update_action(value: int):
    """ PUT method.
        Updates current action value.
        Input: /value/.
    """
    return ControlsBp().update_action(value=value)


@bp_controls.route('/controls/', methods=['GET'])
def controls():
    return ControlsBp().controls()
