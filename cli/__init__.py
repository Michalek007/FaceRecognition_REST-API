""" Cli commands for app.
    Usage:
        from cli import Cli
        cli = Cli(app=app, database=db)
        cli.init()
    Then in shell with activated venv type:
        flask <group_name> <command_name>
    eg: flask app restart
"""
from cli.core import Cli
