import subprocess


class SubprocessApi:
    """ Implements methods allowing to execute commands in shell.
        Api for subprocess lib.
        Attributes:
            root_directory: current directory for all commands (cwd)
            split_output: if True splits run() output string into list
            split_seperator: sep arg for split method
            encoding: name of encoding for run() output
    """
    def __init__(self, root_directory: str = None, split_output: bool = True, split_seperator: bytes = b'\r\n',
                 encoding: str = 'latin-1'):
        self.root_directory = root_directory
        self.split_output = split_output
        self.split_seperator = split_seperator
        self.encoding = encoding

    @staticmethod
    def decoder(data: bytes, split_output: bool = True, split_seperator: bytes = b'\r\n', encoding: str = 'latin-1'):
        """ Decodes bytes to string with given encoding. If error occurs decodes string with 'utf-8'.
            If split_output is True, returns list of strings split with given split_seperator.
            Args:
                data: bytes to decode
                split_output: if True splits string into list with data.split(split_seperator)
                split_seperator: sep arg for split method
                encoding: encoding for encoded bytes data
            Returns:
                list of decoded lines extracted from data (splits with '\\r\\n')
        """
        if not split_output:
            try:
                output = data.decode(encoding=encoding)
            except UnicodeDecodeError:
                output = data.decode()
            return output

        decoded_data = []
        for b in data.split(sep=split_seperator):
            try:
                decoded_data.append(b.decode(encoding=encoding))
            except UnicodeDecodeError:
                decoded_data.append(b.decode(encoding='utf-8'))
        return decoded_data

    def run(self, command, cwd: str = None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, decode_output: bool = True):
        """ Runs command string in shell.
            Args:
                command: string which will be executed in shell
                cwd: directory where the command will be executed
                stdout: stdout stream
                stderr: stderr stream
                decode_output: if True output bytes will be decoded
            Returns:
                tuple (stdout, stderr) - both are list of collected lines (strings)
                or None if directory is incorrect
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
            if not decode_output:
                return stdout_output, stderr_output
            stdout_output = None if stdout_output == b'' else self.decoder(stdout_output, self.split_output, self.split_seperator, self.encoding)
            stderr_output = None if stderr_output == b'' else self.decoder(stderr_output, self.split_output, self.split_seperator, self.encoding)
            return stdout_output, stderr_output
        else:
            return None, None
