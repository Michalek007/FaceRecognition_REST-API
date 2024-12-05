from flask import current_app
from database.schemas import User


class Authenticator:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def validate_user(self):
        """ Checks if user is valid.
            Returns:
                ``None`` if user is valid. otherwise tuple (<message>, <error_code>)
        """
        test_user = User.query.filter_by(username=self.login).first()
        if test_user is None:
            return 'There is no account with that login', 401
        if not current_app.config.get('bcrypt').check_password_hash(test_user.pw_hash, self.password):
            return 'Wrong password', 401
        return None

    def has_acces(self):
        """ Checks if user has access to service.
            Args:
                login: user id
            Returns:
                ``True`` if user has access, ``False`` otherwise
        """
        # TODO: implement -> database user check privilege
        return True
