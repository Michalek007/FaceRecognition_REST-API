from scheduler.tasks import TaskBase
from app.modules.face_recognition import recognize


class FaceRecognitionTask(TaskBase):
    """ main_task -> performs face recognition  """
    def __init__(self, scheduler, api, database, filename: str, user_id: str, image_id: str, aligned: bool):
        super().__init__(scheduler, api, database)
        self.filename = filename
        self.user_id = user_id
        self.image_id = image_id
        self.aligned = aligned

    def main_task(self):
        for job in self.scheduler.get_jobs():
            print(job)
        self.scheduler.remove_job(id=self.image_id)
        for job in self.scheduler.get_jobs():
            print(job)

        response, error = self.api.members_get(user_id=self.user_id)
        if error:
            print(error)
        if response:
            members_list = response.json()
            recognized_names = recognize.run_resnet(self.filename, members_list, self.aligned)
            print(recognized_names)

    def recognize(self):
        pass

    def notification(self, names: list):
        pass
