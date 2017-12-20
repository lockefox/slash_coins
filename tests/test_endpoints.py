"""test_endpoints.py: validate endpoints return as expected"""
from os import path
import json

import pytest
from flask import url_for

import slash_coins._version as _version

@pytest.mark.usefixtures('client_class')
class TestVersionEndpoint:
    """validate /version response"""
    def test_version_happypath(self):
        """test /version normal behavior"""
        req = self.client.get(
            url_for('version')
        )

        raw_data = json.loads(req.data.decode())
        assert raw_data['version'] == _version.__version__
        assert raw_data['app_name'] == _version.PROGNAME
