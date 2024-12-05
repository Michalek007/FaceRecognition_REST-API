from datetime import datetime

from scheduler.tasks import TaskBase
from database.schemas import Acceleration


class AccTask(TaskBase):
    """ main_task -> makes post requests /add_acc/ to service with sample data """

    def main_task(self):
        self.add_acc()

    def add_acc(self):
        response = self.api.add_acc(x=1, y=1, z=9.81)
        if response is None:
            print('Error occurred during adding acc. ')
            return
        print(response.json().get('message'))
