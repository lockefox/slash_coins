"""test_utils.py: validate slash_coins.utils"""
import json
import copy

import pytest
import helpers

import slash_coins.utils as utils
import slash_coins.exceptions as exceptions


class TestPlatform:
    """validate utils.which_platform"""
    def test_platform_slack_happypath(self):
        """validate which_platform() -- SLACK"""
        platform, commands = utils.which_platform(
            request_data={},
            form_data=helpers.SAMPLE_SLACK_JSON
        )

        assert platform == utils.ChatPlatform.slack
        assert commands == ['eth', 'usd']

    def test_platform_hipchat_happypath(self):
        """validate which_platform() -- HipChat"""
        platform, commands = utils.which_platform(
            request_data=json.dumps(helpers.SAMPLE_HIPCHAT_JSON),
            form_data={}
        )

        assert platform == utils.ChatPlatform.hipchat
        assert commands == ['eth', 'usd']

    def test_platform_bad_platform(self):
        """validate which_platform() -- NO PLATFORM"""
        with pytest.raises(exceptions.UnknownChatPlatform):
            platform, commands = utils.which_platform(
                request_data={},
                form_data={}
            )

        bad_slack_payload = copy.deepcopy(helpers.SAMPLE_SLACK_JSON)
        bad_slack_payload['response_url'][0] = 'https://fake.fake.fake/totallyfake'
        with pytest.raises(exceptions.UnknownChatPlatform):
            platform, commands = utils.which_platform(
                request_data={},
                form_data=bad_slack_payload
            )

    def test_platform_bad_command(self):
        """validate which_platform() raises for contents_required"""
        bad_hipchat_payload = copy.deepcopy(helpers.SAMPLE_HIPCHAT_JSON)
        bad_hipchat_payload['item']['message']['message'] = '/test'
        with pytest.raises(exceptions.NoCommandsFound):
            platform, commands = utils.which_platform(
                request_data=json.dumps(bad_hipchat_payload),
                form_data={},
                contents_required=True
            )

        bad_slack_payload = copy.deepcopy(helpers.SAMPLE_SLACK_JSON)
        bad_slack_payload['text'][0] = ''
        with pytest.raises(exceptions.NoCommandsFound):
            platform, commands = utils.which_platform(
                request_data={},
                form_data=bad_slack_payload,
                contents_required=True
            )
