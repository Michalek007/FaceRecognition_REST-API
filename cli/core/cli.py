from cli.groups import GroupType, GroupCreator
from app.modules.service_api import ServiceApi


class Cli:
    """ Cli core class.

        Attributes:
            app: Flask app
            db: database object
            groups: cli groups which will be added to apps
    """
    def __init__(self, app, database):
        self.app = app
        self.db = database
        self.groups = [
            GroupType.App,
            GroupType.Db,
            GroupType.Seed,
        ]

    def init(self):
        """ Cli initialisation.
            Creates cli groups and adds them to app.
        """
        api = ServiceApi()
        for group_type in self.groups:
            GroupCreator.create_group(app=self.app, api=api, database=self.db, group_type=group_type)

        self.add_groups()

    def add_groups(self):
        """ Add cli groups to app. """
        from cli.groups.app import app_cli
        from cli.groups.db import db_cli
        from cli.groups.seed import seed_cli

        self.app.cli.add_command(app_cli)
        self.app.cli.add_command(db_cli)
        self.app.cli.add_command(seed_cli)
