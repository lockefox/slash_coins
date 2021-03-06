"""test_utils.py: validate slash_coins.utils"""
import json
import copy

import pytest
import helpers
import jsonschema

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

class TestGeneratePlatformResponse:
    """validate utils.generate_platform_response()"""
    def test_generate_platform_response_slack(self):
        """validate slack response is correct -- SLACK"""
        response = utils.generate_platform_response(
            'test message',
            utils.ChatPlatform.slack
        )

        jsonschema.validate(response, helpers.SLACK_RESPONSE_SCHEMA)

    def test_generage_platform_response_hipchat(self):
        """validate hipchat response is correct -- HipChat"""
        response = utils.generate_platform_response(
            'test message',
            utils.ChatPlatform.hipchat
        )

        jsonschema.validate(response, helpers.HIPCHAT_RESPONSE_SCHEMA)

    def test_generage_platform_response_bad_platform(self):
        """validate bad-platform exception"""
        with pytest.raises(exceptions.UnknownChatPlatform):
            response = utils.generate_platform_response(
                'test message',
                utils.ChatPlatform.UNKNOWN
            )

def test_name_to_slack_color():
    """validate translation"""
    assert utils.name_to_slack_color('green') == 'good'
    assert utils.name_to_slack_color('yellow') == 'warning'
    assert utils.name_to_slack_color('red') == 'danger'

    assert utils.name_to_slack_color('random') == ''

def test_bot_fail_message():
    """validate fail decoration"""
    assert '/shrug' in utils.bot_fail_message('butts', utils.ChatPlatform.slack)

    assert '(shrug)' in utils.bot_fail_message('butts', utils.ChatPlatform.hipchat)

    assert utils.bot_fail_message('butts', utils.ChatPlatform.UNKNOWN) == 'butts'
