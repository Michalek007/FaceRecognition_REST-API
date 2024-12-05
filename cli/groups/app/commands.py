from cli.groups.app import app_cli
from cli.groups.app.app_group import AppGroup


@app_cli.command('kill')
def kill():
    """ Shuts down server. """
    AppGroup().kill()


@app_cli.command('restart')
def restart():
    """ Restarts server. """
    AppGroup().restart()
