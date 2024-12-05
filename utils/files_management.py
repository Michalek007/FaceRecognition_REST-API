from configuration import Config


class FilesManagement:
    """ Allows to manipulate data from given file.
        When object is created data from file is read and save in attribute 'self.data' as list of lines.
    """
    def __init__(self, file_name, base_dir=Config.BASEDIR):
        self.file_name = file_name
        self.base_dir = base_dir
        self.file = f'{self.base_dir}\\{self.file_name}'
        self.data = []

        self._set_data()

    def _set_data(self):
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
        """ Saves content of attribute 'self.date' to file (overwrites). """
        data_str = '\n'.join(self.data)
        self.overwrite(data_str)
