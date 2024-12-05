import flask_login

from app.blueprints.env_metrics import env_metrics as env_metrics_bp
from app.blueprints.env_metrics.env_metrics_bp import EnvMetricsBp


@env_metrics_bp.route('/env_metrics/<int:env_metrics_id>/', methods=['GET'])
@env_metrics_bp.route('/env_metrics/', methods=['GET'])
def env_metrics(env_metrics_id: int = None):
    """ Returns env metrics with given id or if not specified list of all env metrics from database.
        If given timestamp, returns list of env metrics with later timestamp.
        Input args: /id/, Timestamp.
        Output keys: output {id, temperature, pressure, humidity}
    """
    return EnvMetricsBp().env_metrics(env_metrics_id=env_metrics_id)


@env_metrics_bp.route('/add_env_metrics/', methods=['POST'])
def add_env_metrics():
    """ POST method.
        Adds env metrics to database.
        Input args: Temperature, Pressure, Humidity.
    """
    return EnvMetricsBp().env_metrics_acc()


@env_metrics_bp.route('/delete_env_metrics/', methods=['DELETE'])
@env_metrics_bp.route('/delete_env_metrics/<int:env_metrics_id>/', methods=['DELETE'])
def delete_env_metrics(env_metrics_id: int = None):
    """ DELETE method.
        Delete env metrics with given id or if given timestamp, deletes env metrics with earlier timestamp.
        Input args: /id/, Timestamp.
    """
    return EnvMetricsBp().delete_env_metrics(env_metrics_id=env_metrics_id)


@env_metrics_bp.route('/update_env_metrics/<int:env_metrics_id>/', methods=['PUT'])
def update_env_metrics(env_metrics_id: int = None):
    """ PUT method.
        Updates env metrics with given id.
        Input args: Temperature, Pressure, Humidity.
    """
    return EnvMetricsBp().update_env_metrics(env_metrics_id=env_metrics_id)


@env_metrics_bp.route('/env_metrics_table/', methods=['GET'])
def env_metrics_table():
    return EnvMetricsBp().env_metrics_table()
