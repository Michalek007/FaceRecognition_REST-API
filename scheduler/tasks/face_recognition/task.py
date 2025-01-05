from scheduler.tasks import TaskBase
from app.modules.face_recognition import recognize
from typing import List


class FaceRecognitionTask(TaskBase):
    """ main_task -> performs face recognition  """
    def __init__(self, scheduler, api, database, filename: str, user_id: str, scheduler_job_id: str, aligned: bool, embedding: bool):
        super().__init__(scheduler, api, database)
        self.filename = filename
        self.user_id = user_id
        self.scheduler_job_id = scheduler_job_id
        self.aligned = aligned
        self.embedding = embedding

    def main_task(self):
        for job in self.scheduler.get_jobs():
            print(job)
        self.scheduler.remove_job(id=self.scheduler_job_id)
        for job in self.scheduler.get_jobs():
            print(job)

        response, error = self.api.members_get(user_id=self.user_id)
        if error or not response:
            print(error)
            return
        members_list = response.json()
        if self.embedding:
            recognized_names = recognize.run_lite_face(self.filename, members_list)
        else:
            recognized_names = recognize.run_resnet(self.filename, members_list, self.aligned)
        if not recognized_names:
            return
        if self.aligned or self.embedding:
            response, error = self.api.notifications_set(recognized_names[0], self.user_id)
        else:
            for name in recognized_names:
                response, error = self.api.notifications_set(recognized_names[0], self.user_id)
