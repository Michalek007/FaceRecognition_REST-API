from enum import Enum


class TaskType(Enum):
    # add new task types here
    pass


class TaskCreator:
    """ Contains factory method for tasks. """
    @staticmethod
    def create_task(scheduler, api, database, task_type: TaskType):
        """ Factory method. """
        return None
