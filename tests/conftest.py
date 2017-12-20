"""configtest.py: setup pytest defaults/extensions"""
from os import path

from slash_coins.flask_launcher import APP
import pytest

import prosper.common.prosper_config as p_config

HERE = path.abspath(path.dirname(__file__))
ROOT = path.dirname(HERE)


@pytest.fixture
def app():
    """test fixture for launching/testing Flask endpoints"""
    return APP
