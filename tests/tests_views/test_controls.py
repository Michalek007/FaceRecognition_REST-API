import pytest
from collections import namedtuple

from request_context import RequestContext
from app.blueprints.controls.controls_bp import ControlsBp
from configuration import Config


class TestControls:
    # requests
    def get_action(self):
        return RequestContext.request('/get_action/', ControlsBp(), ControlsBp.get_action)

    def update_action(self, value: int):
        return RequestContext.request('/update_action/', ControlsBp(), ControlsBp.update_action, arg=value, method='PUT')

    # private fixtures
    # tests
    def test_get_action(self):
        return_value = self.get_action()
        expected_value = dict(action=ControlsBp.action)
        assert return_value.json == expected_value

    def test_update_action(self):
        return_value = self.update_action(value=1)
        expected_value = dict(message='Action updated successfully. ')
        assert ControlsBp().action == 1
        assert return_value.json == expected_value
