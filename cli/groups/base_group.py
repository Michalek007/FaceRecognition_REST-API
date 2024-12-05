from abc import ABC


class BaseGroup(ABC):
    """ Base class for all groups classes. """
    _instance = None

    def __new__(cls, app=None, api=None, database=None):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            cls._instance.app = app
            cls._instance.api = api
            cls._instance.db = database
        return cls._instance
