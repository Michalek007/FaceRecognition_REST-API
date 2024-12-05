import pytest
import subprocess

from utils import *

# TODO: make class with constant data used in multiple tests


# utils fixtures
@pytest.fixture
def mock_subprocess_popen(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', lambda *args, **kwargs: None)


@pytest.fixture
def mock_files_management(monkeypatch):
    def mock_set_data(*args, **kwargs):
        # TODO: implement
        pass

    monkeypatch.setattr(FilesManagement, '_set_data', mock_set_data)
    monkeypatch.setattr(FilesManagement, 'overwrite', lambda *args, **kwargs: None)
    monkeypatch.setattr(FilesManagement, 'clear', lambda *args, **kwargs: None)
    monkeypatch.setattr(FilesManagement, 'write_line', lambda *args, **kwargs: None)
