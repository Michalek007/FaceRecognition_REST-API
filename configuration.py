import os
import subprocess
from datetime import datetime, timedelta
from collections import namedtuple
import json


class Config(object):
    """ Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    SCHEDULER_API_ENABLED = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    LISTENER = {
        'host': '127.0.0.1',
        'port': 5000,
    }
    MIN_ACTIVITY_TIME = 15
    PRIVILEGE_ID = 58
    SECRET_KEY = '87673fa7f3a987323301f129'
    TOKEN = '31024daadeb926bc08b0ca0e'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'database\\db\\data.db')
    COMPUTER_NAME = subprocess.Popen('hostname', shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    COMPUTER_NAME = COMPUTER_NAME.replace('\r', '').replace('\n', '')
    CONFIG_FILE = BASEDIR + '\\config.json'

    @staticmethod
    def get_project_details():
        """ Returns name-tuple of project details extracted from json config file. """
        with open(Config.CONFIG_FILE, 'r') as f:
            data = json.loads(f.read(), object_hook=lambda args: namedtuple('X', args.keys())(*args.values()))
        return data


class DevelopmentConfig(Config):
    DEBUG = True
    LOGIN_DISABLED = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    LOGIN_DISABLED = True


class Pid:
    SERVICE = None
