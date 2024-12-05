""" Runs Flask app on development server. """
import os

from app import app, deploy_app_views
from scheduler import deploy_scheduler
from configuration import Pid


if __name__ == '__main__':
    Pid.SERVICE = os.getpid()
    deploy_app_views()
    deploy_scheduler()
    app.run(host='0.0.0.0')
