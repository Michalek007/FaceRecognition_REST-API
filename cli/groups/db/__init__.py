from flask.cli import AppGroup


db_cli = AppGroup('db')

from cli.groups.db.commands import *
