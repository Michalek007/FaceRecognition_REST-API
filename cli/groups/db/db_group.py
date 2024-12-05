from cli.groups import BaseGroup


class DbGroup(BaseGroup):
    """ Implements methods related to database config. """

    def create(self):
        self.db.create_all()
        print('Database created!')

    def drop(self):
        self.db.drop_all()
        print('Database dropped!')
