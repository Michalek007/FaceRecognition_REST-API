from flask.cli import AppGroup


seed_cli = AppGroup('seed')

from cli.groups.seed.commands import *
