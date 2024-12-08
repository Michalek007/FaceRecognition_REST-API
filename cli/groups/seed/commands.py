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


@seed_cli.command('members')
def members():
    """ Seeds members table with tests data. """
    return SeedGroup().members()
