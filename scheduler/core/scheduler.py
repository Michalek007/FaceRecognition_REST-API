from flask_apscheduler import APScheduler

from scheduler.tasks import TaskCreator, TaskType


class Scheduler:
    """ Scheduler adapter class for APScheduler.

        Attributes:
            scheduler: APScheduler object
            db: database object
            api: service api object
            scheduler_jobs: tasks which will be set as scheduler jobs
    """
    def __init__(self, scheduler: APScheduler, api, database):
        self.scheduler = scheduler
        self.db = database
        self.api = api

        # when new task is needed, create new package in scheduler/tasks (base class: BaseTask)
        # and update factory method (TaskCreator) then add correct TaskType to self.scheduler_jobs attribute

        self.scheduler_jobs = [
            {
                'task_type': TaskType.Acc,
                'id': TaskType.Acc.name,
                'minutes': 1
            },
        ]

    def start(self):
        """ Starts scheduler. """
        self.scheduler.start()

    def init_app(self, app):
        """ Initialize scheduler with Flask app. """
        self.scheduler.init_app(app)

    def shut_down(self):
        """ Shuts down scheduler. """
        self.scheduler.shutdown()

    def set_scheduler_jobs(self):
        """ Sets schedulers jobs before running scheduler. """

        for job in self.scheduler_jobs:
            print(job)
            task = TaskCreator.create_task(
                scheduler=self.scheduler,
                api=self.api,
                database=self.db,
                task_type=job.get('task_type')
            )
            self.scheduler.add_job(
                func=task.main_task,
                id=job.get('id'),
                trigger='interval',
                minutes=job.get('minutes')
            )

        for job in self.scheduler.get_jobs():
            print(job)
