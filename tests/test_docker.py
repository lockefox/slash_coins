"""test_docker.py: validate docker container works as expected"""
import io
import json

import pandas as pd
from plumbum import local
import requests
import jsonschema

import pytest
import helpers

import slash_coins._version as _version

DOCKER_UP = False
DOCKER_IMAGE_NAME = 'slash-coin'

LOCAL_ADDRESS = 'http://localhost:{}/'.format(helpers.APP_CONFIG.get('FLASK', 'port'))
@pytest.mark.docker
def test_00_docker_up():
    """validate that docker container is up and running"""
    global DOCKER_UP
    docker = local['docker']
    ps_list = docker('ps')

    docker_list = pd.read_table(
        io.StringIO(ps_list),
        sep=r'\s\s+',
        engine='python'
    )
    print(docker_list)
    DOCKER_UP = any([docker_list['IMAGE'].str.contains(DOCKER_IMAGE_NAME).any()])

    assert DOCKER_UP

@pytest.mark.docker
class TestVersionEndpoint():
    """validate /version"""
    version_address = LOCAL_ADDRESS + 'version'
    def test_version_get(self):
        """validate regular version endpoint"""
        if not DOCKER_UP:
            pytest.xfail('Expected docker image `{}` not running')

        req = requests.get(self.version_address)
        req.raise_for_status()
        version_info = req.json()

        assert version_info['version'] == _version.__version__
        assert version_info['app_name'] == _version.PROGNAME

    def test_version_post_hipchat(self):
        """test response from /version -- HIPCHAT"""
        if not DOCKER_UP:
            pytest.xfail('Expected docker image `{}` not running')

        req = requests.post(
            self.version_address,
            data=json.dumps(helpers.SAMPLE_HIPCHAT_JSON)
        )
        req.raise_for_status()
        jsonschema.validate(req.json(), helpers.HIPCHAT_RESPONSE_SCHEMA)

    def test_version_post_slack(self):
        """test response from /version -- SLACK"""
        if not DOCKER_UP:
            pytest.xfail('Expected docker image `{}` not running')

        req = requests.post(
            self.version_address,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=helpers.SAMPLE_SLACK_JSON
        )
        req.raise_for_status()
        jsonschema.validate(req.json(), helpers.SLACK_RESPONSE_SCHEMA)

@pytest.mark.docker
class TestCoinEndpoint():
    """validate /coins"""
    coins_address = LOCAL_ADDRESS + 'coins'
    def test_coin_post_hipcat(self):
        """test response from /coins -- HIPCHAT"""
        if not DOCKER_UP:
            pytest.xfail('Expected docker image `{}` not running')

        req = requests.post(
            self.coins_address,
            data=json.dumps(helpers.SAMPLE_HIPCHAT_JSON)
        )
        req.raise_for_status()
        jsonschema.validate(req.json(), helpers.HIPCHAT_RESPONSE_SCHEMA)

    def test_coin_post_slack(self):
        """test response from /coins -- SLACK"""
        if not DOCKER_UP:
            pytest.xfail('Expected docker image `{}` not running')

        req = requests.post(
            self.coins_address,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=helpers.SAMPLE_SLACK_JSON
        )
        req.raise_for_status()
        jsonschema.validate(req.json(), helpers.SLACK_RESPONSE_SCHEMA)
