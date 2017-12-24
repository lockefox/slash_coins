"""test_utils.py: validate slash_coins.utils"""
import json

import pytest

import helpers

import slash_coins.utils as utils

class TestPlatform:
    """validate utils.which_platform"""
    def test_platform_slack_happypath(self):
        """validate which_platform() -- SLACK"""
        platform, commands = utils.which_platform(
            request_data={},
            form_data=helpers.SAMPLE_SLACK_JSON
        )

        assert platform == utils.ChatPlatform.slack

    def test_platform_hipchat_happypath(self):
        """validate which_platform() -- HipChat"""
        platform, commands = utils.which_platform(
            request_data=json.dumps(helpers.SAMPLE_HIPCHAT_JSON),
            form_data={}
        )

        assert platform == utils.ChatPlatform.hipchat
