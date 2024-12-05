from datetime import datetime


class DateUtil:
    """ Datetime api. Implements methods related to manipulating dates. """
    def __init__(self, date_format: str, optional_date_format: tuple = None):
        self.date_format = date_format
        self.optional_date_format = optional_date_format

    def from_string(self, date_str: str):
        """ Converts string to date.
            Args:
                date_str: string in date_format or optional_date_format
            Returns:
                datetime object or ``None`` if string does not match date format
        """
        date = None
        try:
            date = datetime.strptime(date_str, self.date_format)
        except ValueError:
            for date_format in self.optional_date_format:
                try:
                    date = datetime.strptime(date_str, date_format)
                    break
                except ValueError:
                    pass
        return date
