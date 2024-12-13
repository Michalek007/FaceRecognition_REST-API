from datetime import datetime
from typing import List


class DateUtil:
    """ Implements methods related to manipulating dates.
        Attributes:
            date_formats: list of date formats by which str dates will be converted (e.g. '%Y-%m-%d %H:%M:%S')
    """
    def __init__(self, date_formats: List[str]):
        self.date_formats = date_formats

    def from_string(self, date_str: str):
        """ Converts string to date. Expected date formats are contained in 'self.date_formats' attribute.
            Args:
                date_str: string containing date
            Returns:
                datetime object or None if string does not match date format
        """
        for date_format in self.date_formats:
            try:
                date = datetime.strptime(date_str, date_format)
            except ValueError:
                continue
            return date
