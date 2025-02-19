from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

from app.modules.service_api import ServiceApi


class TaskBase(ABC):
    """ Base class for all tasks. """
    def __init__(self, scheduler: APScheduler, api: ServiceApi, database: SQLAlchemy):
        self.scheduler = scheduler
        self.api = api
        self.db = database

    @abstractmethod
    def main_task(self):
        """ Method which will be called in scheduler class.
            Should contain main functionalities of task.
        """
        pass
