from enum import Enum

from scheduler.tasks.acc import AccTask


class TaskType(Enum):
    Acc = 0
    # add new task types here


class TaskCreator:
    """ Contains factory method for tasks. """
    @staticmethod
    def create_task(scheduler, api, database, task_type: TaskType):
        """ Factory method. """
        if task_type == TaskType.Acc:
            return AccTask(scheduler=scheduler, api=api, database=database)
        else:
            return None
