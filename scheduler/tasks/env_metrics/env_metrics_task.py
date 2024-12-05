from scheduler.tasks import TaskBase


class EnvMetricsTask(TaskBase):
    """ main_task -> makes post requests add_env_metrics to service """

    def main_task(self):
        self.add_env_metrics()

    def add_env_metrics(self):
        response = self.api.add_env_metrics(temperature=0, pressure=0, humidity=0)
        if response is None:
            print('Error occurred during adding env metrics. ')
            return
        print(response.json().get('message'))

