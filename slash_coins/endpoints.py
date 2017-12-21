"""endpoints.py: REST endpoints

Working off: https://bitbucket.org/travisthetechie/pypples/src/32f79e384133b36ae6883604ce8bfd66e00a5bea/pypples/api/resources.py?at=master&fileviewer=file-view-default

"""
import logging
import json
import platform
import enum

from flask import request
from flask_restful import Resource

import prosper.datareader.coins as coins
from . import _version
from . import exceptions

DEFAULT_LOGGER = logging.getLogger('NULL')
DEFAULT_LOGGER.addHandler(logging.NullHandler())

class ChatPlatform(enum.Enum):
    """help control which platform is talking to app"""
    hipchat = 'hipchat'
    slack = 'slack'
    UNKNOWN = ''

def which_platform(request_data, form_data, logger=DEFAULT_LOGGER):
    """figure out which platform is talking to app

    Args:
        request_data (dict): POST JSON data
        form_data (dict): application/x-www-form-urlencoded data

    Returns:
        enum: ChatPlatform
        list: list of commands

    """
    try:
        args = json.loads(request_data)
    except Exception:
        args = {}
    try:
        form = dict(form_data)
    except Exception:
        form = {}

    mode = ChatPlatform.UNKNOWN
    if args:
        mode = ChatPlatform.hipchat
        logger.info(
            '--HIPCHAT METADATA: user=@%s channel=%s chat=%s',
            args['item']['message']['from']['mention_name'],
            args['item']['room']['name'],
            args['item']['room']['links']['self']
        )

    if any([bool('hooks.slack.com' in resp) for resp in form['response_url']]):
        # TODO: validate slack token
        mode = ChatPlatform.slack
        logger.info(
            '--SLACK METADATA: user=@%s channel=%s chat=%s',
            form['user_name'],
            form['channel_name'],
            form['team_domain']
        )

    commands = parse_slash_args(mode, args, form)

    return mode, commands

def parse_slash_args(mode, request_data, form_data):
    """figure out what's on the line after the slash

    Args:
        mode (enum): which platform is the app talking to
        request_data (:obj:`dict`): POST JSON data
        form_data (:obj:`dict`): urlencode data

    Returns:
        list: list of stuff after the /command

    """
    if mode == ChatPlatform.hipchat:
        args_list = request_data['event']['item']['message']['message'].split()
        return args_list[:1]  #drop /command

    if mode == ChatPlatform.slack:
        args_list = form_data['text'][0].split()

    raise exceptions.UnknownChatPlatform('Unable to parse request')

class Root(Resource):
    """root path"""
    def get(self):
        """HTTP GET behavior"""
        logger = logging.getLogger(_version.PROGNAME)
        logger.info('ROOT request')
        logger.debug(request.data)
        return {
            'result': 'OK'
        }

class Version(Resource):
    """return version information about app"""
    def get(self):
        """HTTP GET behavior"""
        logger = logging.getLogger(_version.PROGNAME)  # TODO: parent class + @property
        logger.info('VERSION request')
        return {
            'version': _version.__version__,
            'app_name': _version.PROGNAME
        }
    def post(self):
        """HTTP POST -- respond via /command"""
        pass

class CoinQuote(Resource):
    """generate quote for desired cryptocoin"""
    def post(self):
        """HTTP POST behavior"""
        logger = logging.getLogger(_version.PROGNAME)  # TODO: parent class + @property

        # Figure out what's coming in #
        try:
            mode, commands = which_platform(request.data, request.form, logger=logger)
        except Exception:
            logger.error('COINQUOTE -- INVALID PLATFORM REQUEST', exc_info=True)
            return

        logger.info('COINQUOTE request @%s: %s', mode, commands)

        return {
            'color': 'green',
            'message': 'It\'s going to be sunny tomorrow! (yey)',
            'notify': False,
            'message_format': 'text'
        }
