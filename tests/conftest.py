"""configtest.py: setup pytest defaults/extensions"""
from os import path

from slash_coins import create_app
import pytest

import prosper.common.prosper_config as p_config

HERE = path.abspath(path.dirname(__file__))
ROOT = path.dirname(HERE)


@pytest.fixture
def app():
    my_app = create_app(
        local_configs=p_config.ProsperConfig(
            path.join(ROOT, 'scripts', 'app.cfg')
        ),
        testmode=True
    )
    return my_app
