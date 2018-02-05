"""test_endpoints.py: validate endpoints return as expected"""
from os import path
import json
import copy

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

    def test_version_slack(self):
        """make sure /version POST endpoint works as advertised -- SLACK"""
        req = self.client.post(
            url_for('version'),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=helpers.SAMPLE_SLACK_JSON
        )
        jsonschema.validate(req.json, helpers.SLACK_RESPONSE_SCHEMA)
        # TODO: validate contents

    def test_version_hipchat(self):
        """make sure /version POST endpoint works as advertised -- HIPCHAT"""
        req = self.client.post(
            url_for('version'),
            data=json.dumps(helpers.SAMPLE_HIPCHAT_JSON)
        )
        jsonschema.validate(req.json, helpers.HIPCHAT_RESPONSE_SCHEMA)
        # TODO: validate contents

    def test_version_unknown(self):
        """make sure /version POST endpoint works as advertised -- UNKNOWN"""
        req = self.client.post(
            url_for('version'),
            data=''
        )
        assert not req.json


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

    def test_coinquote_unknown(self):
        """test /coins normal behavior -- SLACK"""
        req = self.client.post(
            url_for('coinquote'),
            data=''
        )
        assert not req.json

    def test_coinquote_bad_ticker_hipchat(self):
        """validate unkown ticker -- HIPCHAT"""
        bad_hipchat_json = copy.deepcopy(helpers.SAMPLE_HIPCHAT_JSON)
        bad_hipchat_json['item']['message']['message'] = '/test fakecoin'

        req = self.client.post(
            url_for('coinquote'),
            data=json.dumps(bad_hipchat_json)
        )

        jsonschema.validate(req.json, helpers.HIPCHAT_RESPONSE_SCHEMA)
        assert req.json['message'] == 'Can\'t resolve \'[\'fakecoin\']\' (shrug)'

    def test_coinquote_bad_ticker_slack(self):
        """validate unkown ticker -- SLACK"""
        bad_slack_json = copy.deepcopy(helpers.SAMPLE_SLACK_JSON)
        bad_slack_json['text'][0] = 'fakecoin'

        req = self.client.post(
            url_for('coinquote'),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=bad_slack_json
        )

        jsonschema.validate(req.json, helpers.SLACK_RESPONSE_SCHEMA)
        assert req.json['text'] == '/shrug Can\'t resolve \'[\'fakecoin\']\''


@pytest.mark.usefixtures('client_class')
class TestStockQuoteEndpoint:
    """validate /stocks response"""
    def test_stockquote_happypath_hipchat(self):
        """test /stocks normal behavior -- HIPCHAT"""
        hipchat_json = copy.deepcopy(helpers.SAMPLE_HIPCHAT_JSON)
        hipchat_json['item']['message']['message'] = '/test AAPL'

        req = self.client.post(
            url_for('stockquote'),
            data=json.dumps(hipchat_json)
        )
        jsonschema.validate(req.json, helpers.HIPCHAT_RESPONSE_SCHEMA)
        assert 'Apple Inc.' in req.json['message']

    def test_stockquote_happypath_slack(self):
        """test /stocks normal behavior -- SLACK"""
        slack_json = copy.deepcopy(helpers.SAMPLE_SLACK_JSON)
        slack_json['text'] = ['AAPL']

        req = self.client.post(
            url_for('stockquote'),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=slack_json
        )

        jsonschema.validate(req.json, helpers.SLACK_RESPONSE_SCHEMA)
        assert 'Apple Inc.' in req.json['text']

    def test_stockquote_unkown(self):
        """test empty behavior -- SLACK"""
        req = self.client.post(
            url_for('stockquote'),
            data=''
        )
        assert not req.json

    def test_stockquote_bad_ticker_hipchat(self):
        """validate /stocks bad behavior -- HIPCHAT"""
        bad_hipchat_json = copy.deepcopy(helpers.SAMPLE_HIPCHAT_JSON)
        bad_hipchat_json['item']['message']['message'] = '/test BUTTS'

        req = self.client.post(
            url_for('stockquote'),
            data=json.dumps(bad_hipchat_json)
        )

        jsonschema.validate(req.json, helpers.HIPCHAT_RESPONSE_SCHEMA)
        assert req.json['message'] == 'Can\'t resolve \'[\'BUTTS\']\' (shrug)'

    def test_stockquote_bad_ticker_slack(self):
        """validate unkown ticker -- SLACK"""
        bad_slack_json = copy.deepcopy(helpers.SAMPLE_SLACK_JSON)
        bad_slack_json['text'][0] = 'BUTTS'

        req = self.client.post(
            url_for('stockquote'),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=bad_slack_json
        )

        jsonschema.validate(req.json, helpers.SLACK_RESPONSE_SCHEMA)
        assert req.json['text'] == '/shrug Can\'t resolve \'[\'BUTTS\']\''
