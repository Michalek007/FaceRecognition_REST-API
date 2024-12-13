from enum import Enum

from scheduler.tasks.face_recognition import FaceRecognitionTask


class TaskType(Enum):
    # add new task types here
    face_recognition = 0


class TaskCreator:
    """ Contains factory method for tasks. """
    TASKS = {
        TaskType.face_recognition: FaceRecognitionTask,
    }

    @classmethod
    def create_task(cls, scheduler, api, database, task_type: TaskType, *args, **kwargs):
        """ Factory method. """

        task = cls.TASKS.get(task_type)
        return task(scheduler, api, database, *args, **kwargs) if task is not None else None
