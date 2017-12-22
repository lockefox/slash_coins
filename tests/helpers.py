"""helpers.py: tests global scratch space"""
from os import path
import uuid

import shortuuid


HERE = path.abspath(path.dirname(__file__))
ROOT = path.dirname(HERE)

SAMPLE_HIPCHAT_JSON = {
    'event': 'room_message',
    'item': {
        'message': {
            'date': '2017-12-20T23:35:22.234819+00:00',
            'from': {
                'id': 999,
                'links': {
                    'self': 'https://fake.hipchat.com/v2/user/500'
                },
                'mention_name': 'TestUser',
                'name': 'Test User',
                'version': 'N0TUSED',
            },
            'id': str(uuid.uuid1()),
            'mentions': [],
            'message': '/test eth usd',
            'type': 'message'
        },
        'room': {
            'id': 9999,
            'is_archived': False,
            'links': {
                'members': 'https://fake.hipchat.com/v2/room/9999/member',
                'participants': 'https://fake.hipchat.com/v2/room/9999/participant',
                'self': 'https://fake.hipchat.com/v2/room/9999',
                'webhooks': 'https://fake.hipchat.com/v2/room/9999/webhook'
            },
            'name': 'TestChatRoom',
            'privacy': 'private',
            'version': 'N0TUSED'
        }
    },
    'oauth_client_id': str(uuid.uuid1()),
    'webhook_id': 800
}
HIPCHAT_RESPONSE_SCHEMA = {
    'type':'object',
    'properties': {
        'color': {'type':'string', 'enum':['yellow', 'green', 'red', 'purple', 'gray', 'random']},
        'message': {'type':'string'},
        'notify': {'type':'boolean'},
        'message_format': {'type':'string', 'enum':['text']}
    },
    'required': ['color', 'message', 'notify', 'message_format'],
    'additionalProperties': False
}


SAMPLE_SLACK_JSON = {
    'token': [str(shortuuid.uuid())],
    'team_id': ['FAKETEAM1'],
    'team_domain': ['test_domain'],
    'channel_id': ['FAKECHAN1'],
    'channel_name': ['test_channel'],
    'user_id': ['FAKEUSER1'],
    'user_name': ['test_user'],
    'command': ['/test'],
    'text': ['eth usd'],
    'response_url': [
        'https://hooks.slack.com/commands/FAKETEAM1/999999999999/' + shortuuid.uuid()],
    'trigger_id': [
        '999999999999.99999999999.' + shortuuid.ShortUUID().random(length=32)]
}
SLACK_RESPONSE_SCHEMA = {
    'type':'object',
    'properties': {
        'text': {'type':'string'},
        'attachments': {
            'type':'object',
            'properties':{
                'fallback': {'type':'string'},
                'color': {'type':'string', 'enum':['good', 'warning', 'danger']}
            },
            'required':['fallback']
        }
    },
    'required': ['text', 'attachments'],
    'additionalProperties': False
}
