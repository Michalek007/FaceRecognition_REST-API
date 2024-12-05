import pytest
import psutil
import datetime

from request_context import RequestContext
from app.blueprints.user.user_bp import UserBp
from database.schemas import user_schema, users_schema, User


class TestUser:
    # requests
    def register(self, method,  **kwargs):
        return RequestContext.request('/register/', UserBp(), UserBp.register, query_string=kwargs, method=method)

    def users(self, user_id: int = None):
        return RequestContext.request('/register/', UserBp(), UserBp.users, arg=user_id)

    # private fixtures
    @pytest.fixture
    def mock_user_query_all(self, monkeypatch):
        monkeypatch.setattr(User, 'query_all', lambda *args, **kwargs: [
            User(id=1, username='test', pw_hash='test'),
            User(id=2, username='test1', pw_hash='test')
        ])

    # tests
    def test_register_no_values(self):
        return_value = self.register('POST')
        expected_value = {'message': 'No value. Expected values for keys: \'login\', \'password\', \'repeat_password\''}
        assert return_value[0].json == expected_value
        assert return_value[1] == 400

    # def test_users(self, mock_user_query_all):
    #     return_value = self.users()
    #     expected_value = {'users': [
    #         dict(id=1, username='test', pw_hash='test'),
    #         dict(id=2, username='test1', pw_hash='test')
    #     ]}
    #     assert return_value.json == expected_value
