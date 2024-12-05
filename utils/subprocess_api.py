import subprocess

from configuration import Config


class SubprocessApi:
    """ Implements methods allowing to execute commands in shell.
        Api for subprocess lib.
    """
    def __init__(self, root_directory: str = Config.BASEDIR):
        self.root_directory = root_directory

    @staticmethod
    def decoder(data: bytes):
        """ Decodes bytes to string.
            Args:
                data: bytes to decode
            Returns:
                list of decoded lines extracted from data
        """
        decoded_data = []
        for b in data.split(b'\r\n'):
            try:
                decoded_data.append(bytes.decode(b, 'latin-1'))
            except UnicodeDecodeError:
                decoded_data.append(bytes.decode(b))
        return decoded_data

    def run(self, command, cwd: str = None, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        """ Runs command string in shell.
            Args:
                command: string which will be executed in shell
                cwd: directory where the command will be executed
                stdout: stdout stream
                stderr: stderr stream
            Returns:
                tuple (stdout, stderr) - both are list of collected lines (strings)
                or ``None`` if directory is incorrect
        """
        # if stdout or stderr is None it prints output where your script prints
        # if stdout or stderr is subprocess.Pipe u can extract output with <your_popen_obj>.communicate() method
        # you can pass any file-like object to stdout and stderr
        if cwd is None:
            cwd = self.root_directory
        try:
            process = subprocess.Popen(command,
                                       shell=True,
                                       cwd=cwd,
                                       stdout=stdout,
                                       stderr=stderr)
        except NotADirectoryError:
            return None
        if stdout is not None or stderr is not None:
            stdout_output, stderr_output = process.communicate()
            stdout_output = None if stdout_output == b'' else self.decoder(stdout_output)
            stderr_output = None if stderr_output == b'' else self.decoder(stderr_output)
            return stdout_output, stderr_output
        else:
            return None, None
