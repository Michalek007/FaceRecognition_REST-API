import flask_login

from app.blueprints.config import config
from app.blueprints.config.config_bp import ConfigBp


@config.route('/get_pid/', methods=['GET'])
def get_pid():
    """ Returns process pid of service.
        Output keys: SERVICE.
    """
    return ConfigBp().get_pid()


@config.route('/kill/', methods=['GET'])
def kill():
    """ Shuts down service. For development purposes. """
    return ConfigBp().kill()


@config.route('/restart/', methods=['GET'])
def restart():
    """ Restarts service. For development purposes. """
    return ConfigBp().restart()


@config.route('/settings/')
def settings():
    return ConfigBp().settings()
