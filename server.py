""" Deploys Flask app as wsgi server. """
from gevent.monkey import patch_all; patch_all()
from gevent import pywsgi
import os

from app import app, deploy_app_views
from scheduler import deploy_scheduler
from configuration import Pid

server_wsgi = pywsgi.WSGIServer(listener=('0.0.0.0', app.config['LISTENER']['port']), application=app)


def run(server):
    return server.serve_forever()


if __name__ == '__main__':
    Pid.SERVICE = os.getpid()
    deploy_app_views()
    deploy_scheduler()
    run(server_wsgi)
