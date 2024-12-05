from enum import Enum

from cli.groups.app.app_group import AppGroup
from cli.groups.db.db_group import DbGroup
from cli.groups.seed.seed_group import SeedGroup


class GroupType(Enum):
    App = 0
    Db = 1
    Seed = 2
    # add new group types here


class GroupCreator:
    """ Contains factory method for cli groups. """
    @staticmethod
    def create_group(app, api, database, group_type: GroupType):
        """ Factory method. """
        if group_type == GroupType.App:
            return AppGroup(app=app, api=api, database=database)
        elif group_type == GroupType.Db:
            return DbGroup(app=app, api=api, database=database)
        elif group_type == GroupType.Seed:
            return SeedGroup(app=app, api=api, database=database)
        else:
            return None
