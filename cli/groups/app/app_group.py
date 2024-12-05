from cli.groups import BaseGroup
from utils import ProcessUtil, SubprocessApi
from configuration import Config, Pid


class AppGroup(BaseGroup):
    """ Implements method related to app config. """

    def kill(self):
        self.api.kill()
        print('Service is shut down!')

    def restart(self):
        self.api.restart()
        print('Service is restarting!')
