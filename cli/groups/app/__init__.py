from flask.cli import AppGroup


app_cli = AppGroup('app')

from cli.groups.app.commands import *
