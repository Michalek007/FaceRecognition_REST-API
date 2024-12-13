import os
from datetime import datetime, timedelta
from collections import namedtuple
import json
from pathlib import Path
import socket
import secret


class Config:
    """ Configuration base, for all environments. """
    DEBUG = False
    TESTING = False
    SCHEDULER_API_ENABLED = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    LISTENER = {
        'host': '127.0.0.1',
        'port': 5000,
    }
    MIN_ACTIVITY_TIME = 15
    SECRET_KEY = secret.SECRET_KEY
    TOKEN = secret.TOKEN
    COMPUTER_NAME = socket.gethostname()
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE = os.path.join(BASEDIR, str(Path('database/data/database.db')))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
    CONFIG_FILE = os.path.join(BASEDIR, 'config.json')
    RUN_FILE = os.path.join(BASEDIR, 'run.bat')
    RESTART_SCRIPT = os.path.join(BASEDIR, str(Path('scripts/restartService.bat')))
    TEMP_UPLOAD_DIR = os.path.join(BASEDIR, str(Path('app/static/temp')))
    IMAGES_DIR = os.path.join(BASEDIR, str(Path('database/data/images')))
    EMBEDDINGS_DIR = os.path.join(BASEDIR, str(Path('database/data/embeddings')))

    for path in (TEMP_UPLOAD_DIR, IMAGES_DIR, EMBEDDINGS_DIR):
        path_obj = Path(path)
        path_obj.mkdir(parents=True, exist_ok=True)

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
