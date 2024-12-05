import pytest
from collections import namedtuple

from request_context import RequestContext
from app.blueprints.details.details_bp import DetailsBp
from configuration import Config


class TestDetails:
    # requests
    def app_details(self):
        return RequestContext.request('/app_details/', DetailsBp(), DetailsBp.app_details)

    def help(self, method=None):
        return RequestContext.request('/help/', DetailsBp(), DetailsBp.help, arg=method)

    # private fixtures
    @pytest.fixture
    def mock_get_project_details(self, monkeypatch):
        class MockProjectDetails:
            metadata = namedtuple('Metadata', 'VERSION PROJECT_NAME')('2.0.0.0', 'REST-API')
        monkeypatch.setattr(Config, 'get_project_details', lambda *args, **kwargs: MockProjectDetails())

    @pytest.fixture
    def mock_get_service_methods(self, monkeypatch):
        def mock_method1():
            """ Mock docs for method1.
                Second line.
                Third line.
            """
            return None

        def mock_method2():
            """ Mock docs for method2.
                Second line.
                Third line.
            """
            return None
        monkeypatch.setattr(DetailsBp, 'get_service_methods', lambda *args, **kwargs: [mock_method1, mock_method2])

    # tests
    def test_app_details(self, mock_get_project_details):
        return_value = self.app_details()
        expected_value = dict(
            ProjectName='REST-API',
            Version='2.0.0.0',
            RootDirectory=Config.BASEDIR,
            HostName=Config.COMPUTER_NAME
        )
        assert return_value.json == expected_value

    def test_help(self, mock_get_service_methods):
        return_value = self.help()
        expected_value = dict(
            api_methods={
                'mock_method1': 'Mock docs for method1. Second line. Third line.',
                'mock_method2': 'Mock docs for method2. Second line. Third line.',
            }
        )
        assert return_value.json == expected_value

    def test_help_method1(self, mock_get_service_methods):
        method = 'mock_method1'
        return_value = self.help(method=method)
        expected_value = {method: 'Mock docs for method1. Second line. Third line.'}
        assert return_value.json == expected_value

    def test_help_wrong_method(self, mock_get_service_methods):
        return_value = self.help(method='wrong_method')
        expected_value = {'message': 'There is no method in api with that name.'}
        assert return_value[0].json == expected_value
        assert return_value[1] == 404
