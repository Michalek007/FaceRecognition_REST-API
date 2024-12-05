import pytest

from request_context import RequestContext
from app.blueprints.config.config_bp import ConfigBp
from configuration import Pid
from utils import SubprocessApi, ProcessUtil


class TestConfig:
    # requests
    def get_pid(self):
        return RequestContext.request('/get_pid/', ConfigBp(), ConfigBp.get_pid)

    def kill(self):
        return RequestContext.request('/kill/', ConfigBp(), ConfigBp.kill)

    def restart(self):
        return RequestContext.request('/restart/', ConfigBp(), ConfigBp.restart)

    # private fixtures
    @pytest.fixture
    def mock_process_util_task_kill(self, monkeypatch):
        monkeypatch.setattr(ProcessUtil, 'task_kill', lambda *args, **kwargs: None)

    @pytest.fixture
    def mock_subprocess_api_run(self, monkeypatch):
        monkeypatch.setattr(SubprocessApi, 'run', lambda *args, **kwargs: None)

    # tests
    def test_get_pid(self):
        Pid.SERVICE = 421
        return_value = self.get_pid()
        expected_value = {'SERVICE': 421}
        assert return_value.json == expected_value

    def test_kill(self, mock_process_util_task_kill):
        return_value = self.kill()
        expected_value = {'message': 'Service is shut down!'}
        assert return_value.json == expected_value

    def test_restart(self, mock_process_util_task_kill, mock_subprocess_api_run):
        return_value = self.restart()
        expected_value = {'message': 'Service is restarting!'}
        assert return_value.json == expected_value
