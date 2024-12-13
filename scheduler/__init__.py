""" Scheduler with periodic tasks.
    Usage:
        from scheduler import deploy_scheduler
        deploy_scheduler()
    Important: should be used before running Flask app
"""
from flask_apscheduler import APScheduler

from app import app, db
from scheduler.core import Scheduler
from app.modules.service_api import ServiceApi


def deploy_scheduler():
    """ Deploys scheduler. Should be called before running app. """

    api = ServiceApi()
    scheduler = Scheduler(
        scheduler=APScheduler(),
        api=api,
        database=db
    )
    scheduler.init_app(app)
    scheduler.set_scheduler_jobs()
    scheduler.start()
    print("Scheduler deployed!")
