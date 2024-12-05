import flask_login

from app.blueprints.details import details
from app.blueprints.details.details_bp import DetailsBp


@details.route('/app_details/', methods=['GET'])
def app_details():
    """ Returns project details.
        Output keys: ProjectName, Version, RootDirectory, HostName.
    """
    return DetailsBp().app_details()


@details.route('/help/', methods=['GET'])
@details.route('/help/<method>/', methods=['GET'])
def help(method=None):
    """ Returns docs for given method or if not specified list of docs for all service methods.
        Input args: /method/.
        Output keys: api_methods: {<method_name>} or <method_name>.
    """
    return DetailsBp().help(method=method)


@details.route('/info/')
def info():
    return DetailsBp().info()


@details.route('/methods/')
def methods():
    return DetailsBp().methods()
