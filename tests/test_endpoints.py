"""test_endpoints.py: validate endpoints return as expected"""
from os import path
import json

import jsonschema
import pytest
from flask import url_for

import slash_coins._version as _version
import helpers


@pytest.mark.usefixtures('client_class')
class TestVersionEndpoint:
    """validate /version response"""
    def test_version_happypath(self):
        """test /version normal behavior"""
        req = self.client.get(
            url_for('version')
        )

        assert req.json['version'] == _version.__version__
        assert req.json['app_name'] == _version.PROGNAME

@pytest.mark.usefixtures('client_class')
class TestCoinQuoteEndpoint:
    """validate /coins response"""
    def test_coinquote_happypath_hipchat(self):
        """test /coins normal behavior -- HIPCHAT"""
        req = self.client.post(
            url_for('coinquote'),
            data=json.dumps(helpers.SAMPLE_HIPCHAT_JSON)
        )

        jsonschema.validate(req.json, helpers.HIPCHAT_RESPONSE_SCHEMA)
        assert 'Ethereum' in req.json['message']

    def test_coinquote_happypath_slack(self):
        """test /coins normal behavior -- SLACK"""
        req = self.client.post(
            url_for('coinquote'),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=helpers.SAMPLE_SLACK_JSON
        )

        jsonschema.validate(req.json, helpers.SLACK_RESPONSE_SCHEMA)
        assert 'Ethereum' in req.json['text']
