import flask_login


class User(flask_login.UserMixin):
    """ Default Flask user. """
    pass
    # def is_active(self):
    #     """True, as all users are active."""
    #     return True
    #
    # def get_id(self):
    #     """Return the email address to satisfy Flask-Login's requirements."""
    #     return self.email
    #
    # def is_authenticated(self):
    #     """Return True if the user is authenticated."""
    #     return self.authenticated
    #
    # def is_anonymous(self):
    #     """False, as anonymous users aren't supported."""
    #     return False
