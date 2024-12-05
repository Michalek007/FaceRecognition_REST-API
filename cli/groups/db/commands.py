from cli.groups.db import db_cli
from cli.groups.db.db_group import DbGroup


@db_cli.command('create')
def create():
    """ Creates all database tables. """
    return DbGroup().create()


@db_cli.command('drop')
def drop():
    """ Drops all database tables. """
    return DbGroup().drop()
