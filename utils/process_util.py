from utils import SubprocessApi
from configuration import Pid


class ProcessUtil:
    """ Implements methods for process management. """
    def __init__(self):
        self.subprocess = SubprocessApi()

    def find_process(self, pid: int):
        """ Searches for process with given pid.
            Args:
                pid: pid value of searched process
            Returns:
                ``True`` if process exist, ``False`` otherwise.
        """
        pid = str(pid)
        stdout, stderr = self.subprocess.run('tasklist')
        pids = []
        for process in stdout:
            process = process.split(' ')
            for item in process:
                if item.isnumeric():
                    pids.append(item)
                    break
        return pid in pids

    def task_kill(self, pid: int, capture_output=False):
        """ Kills process with given pid.
            Args:
                pid: pid value of searched process
                capture_output: if False output is ignored
            Returns:
                tuple (stdout, stderr) if capture_output is ``True`` otherwise ``None``
        """
        # if pid != Pid.SERVICE:
        #     return None
        if capture_output:
            stdout, stderr = self.subprocess.run(f'taskkill /pid:{pid} /F')
            return stdout, stderr
        self.subprocess.run(f'taskkill /pid:{pid} /F', stdout=None, stderr=None)
