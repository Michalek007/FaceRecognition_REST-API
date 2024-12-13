import os
import shutil
from pathlib import Path
from typing import Union


class FileManager:
    """ Allows to manipulate data from given file.
        When object is created data from file is read and save in attribute 'self.data' as list of lines.
        Implements static methods for creating, deleting dirs & files.
        Attributes:
            filename: path or name of file
            basedir: optional base directory
            data: list of lines extracted from file
    """
    def __init__(self, filename: str, basedir: str = None):
        self.filename = filename
        self.basedir = basedir
        if basedir:
            self.file = Path(f'{self.basedir}/{self.filename}')
        else:
            self.file = filename
        self.data = []

        self._set_data()

    @staticmethod
    def create_dir(directory: str):
        """ Creates given directory.
            Returns:
                error if occurred, None otherwise
        """
        try:
            os.mkdir(directory)
        except FileExistsError:
            return None
        except OSError as err:
            return err
        return None

    @staticmethod
    def create_file(filename: str, content: Union[str, bytes], basedir: str = None, binary: bool = False):
        """ Creates given file. If exist it will be truncated.
            Returns:
                error if occurred, None otherwise
        """
        if basedir:
            filename = os.path.join(basedir, filename)
        mode = 'wb' if binary else 'w'
        try:
            with open(filename, mode) as f:
                f.write(content)
        except OSError as err:
            return err
        return None

    @staticmethod
    def delete_dir(directory: str):
        """ Deletes whole directory (with all files/dirs in it).
            Returns:
                error if occurred, None otherwise
        """
        try:
            shutil.rmtree(directory)
        except OSError as err:
            return err
        return None

    @staticmethod
    def delete_file(filename: str, basedir: str = None):
        """ Deletes given file. If not exists error will not be raised.
            Returns:
                error if occurred, None otherwise
        """
        if basedir:
            filename = os.path.join(basedir, filename)
        try:
            path = Path(filename)
            path.unlink(missing_ok=True)
        except OSError as err:
            return err
        return None

    def _set_data(self):
        """ Sets 'self.data' attribute with lines extracted from file. """
        with open(self.file, 'r') as f:
            self.data = f.read().split('\n')

    def overwrite(self, data):
        """ Overwrites file with given data. """
        with open(self.file, 'w') as f:
            f.write(data)
        self._set_data()

    def clear(self):
        """ Completely clears file. """
        with open(self.file, 'r+') as f:
            f.truncate(0)
        self._set_data()

    def write_line(self, data: str):
        """ Adds line to the end of file. """
        with open(self.file, 'a') as f:
            f.write(data + '\n')
        self._set_data()

    def get_data(self):
        """ Returns extracted data from file. """
        return self.data

    def save_data(self):
        """ Saves content of attribute 'self.data' to file (overwrites). """
        data_str = '\n'.join(self.data)
        self.overwrite(data_str)
