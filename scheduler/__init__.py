""" Scheduler with periodic tasks.
    Usage:
        from scheduler import deploy_scheduler
        deploy_scheduler()
    Important: should be used before running Flask app
"""
from flask_apscheduler import APScheduler

from app import app, db
from scheduler.core import Scheduler
from utils import ServiceRequestsApi


def deploy_scheduler():
    """ Deploys scheduler. Should be called before running app. """

    api = ServiceRequestsApi()
    scheduler = Scheduler(
        scheduler=APScheduler(),
        api=api,
        database=db
    )
    scheduler.init_app(app)
    scheduler.set_scheduler_jobs()
    scheduler.start()
    print("Scheduler deployed!")
