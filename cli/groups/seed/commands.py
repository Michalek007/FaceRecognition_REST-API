from cli.groups.seed import seed_cli
from cli.groups.seed.seed_group import SeedGroup


@seed_cli.command('init')
def init():
    """ Initialises database table with necessary data. """
    return SeedGroup().init()


@seed_cli.command('users')
def users():
    """ Seeds users table with tests data. """
    return SeedGroup().users()


@seed_cli.command('acc')
def acc():
    """ Seeds acc table with tests data. """
    return SeedGroup().acc()


@seed_cli.command('env_metrics')
def env_metrics():
    """ Seeds env_metrics table with tests data. """
    return SeedGroup().env_metrics()
