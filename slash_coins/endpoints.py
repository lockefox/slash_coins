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

def which_platform(
        request_data,
        form_data,
        contents_required=False,
        logger=DEFAULT_LOGGER,
):
    """figure out which platform is talking to app

    Args:
        request_data (dict): POST JSON data
        form_data (dict): application/x-www-form-urlencoded data
        command_required (bool): is content expected after /command
        logger (:obj:`logging.logger`): logging handle

    Returns:
        enum: ChatPlatform
        list: list of commands

    Raises:
        UnkownChatPlatform: Unable to decide /command source
        NoCommandsFound: no data found after /command

    """
    try:
        args = json.loads(request_data)
    except Exception:
        args = {}
    try:
        form = dict(form_data)
    except Exception:
        form = {}

    logger.debug(form)
    mode = ChatPlatform.UNKNOWN
    commands = []
    if args:
        mode = ChatPlatform.hipchat
        commands = args['item']['message']['message'].split()
        commands = commands[1:]  # drop /text
        logger.info(
            '--HIPCHAT METADATA: user=@%s channel=%s chat=%s',
            args['item']['message']['from']['mention_name'],
            args['item']['room']['name'],
            args['item']['room']['links']['self']
        )

    elif 'hooks.slack.com/commands' in form['response_url'][0]:
        # TODO: validate slack token
        mode = ChatPlatform.slack
        commands = form['text'][0].split()
        logger.info(
            '--SLACK METADATA: user=@%s channel=%s chat=%s',
            form['user_name'][0],
            form['channel_name'][0],
            form['team_domain'][0]
        )
    else:
        logger.warning('Unable to decipher chat platform')
        mode = ChatPlatform.UNKNOWN

    if mode == ChatPlatform.UNKNOWN:
        raise exceptions.UnkownChatPlatform('Unable to parse which chat /command came from')
    if not commands and contents_required:
        raise exceptions.NoCommandsFound('Empty command string recieved')

    return mode, commands

def generate_platform_response(
        message,
        mode,
        do_code=False,
        color='green',
):
    """pipe out results with platform-specific wrapping

    Args:
        message (str): chat response
        mode (enum): which platform to respond to
        do_code (bool): wrap response with code preformatting
        color (str): color response

    Returns:
        dict: json repsonse

    """
    if mode == ChatPlatform.hipchat:
        if do_code:
            message = '/code {}'.format(message)
        return {
            'color': color,
            'message': message,
            'notify': False,
            'message_format': 'text'
        }

    if mode == ChatPlatform.slack:
        main_message = message
        if do_code:
            main_message = '`{}`'.format(message)
        response = {
            'text': main_message,
            'attachments':{
                'fallback': message,
            }
        }
        slack_color = name_to_slack_color(color)
        if slack_color:
            response['attachments']['color'] = slack_color

        return response

    raise exceptions.UnknownChatPlatform('Cannot build response')

def name_to_slack_color(color_name):
    """map hipchat color-names to slack colors

    Args:
        color_name (str): name of color

    Returns:
        str: slack color name

    """
    color_name = color_name.lower()
    if color_name == 'green':
        return 'good'
    if color_name == 'yellow':
        return 'warning'
    if color_name == 'red':
        return 'danger'

    return ''

def bot_fail_message(message, mode):
    """generate useful sorry message

    Args
        message (str): error message
        mode (enum): which platform to respond to

    Returns:
        str: error response

    """
    if mode == ChatPlatform.hipchat:
        return '{} (shrug)'.format(message)

    if mode == ChatPlatform.slack:
        return '/shrug {}'.format(message)

    return message


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
            mode, commands = which_platform(
                request.data, request.form, contents_required=True,logger=logger
            )
        except Exception:
            logger.warning('COINQUOTE -- INVALID PLATFORM REQUEST', exc_info=True)
            return

        logger.info('COINQUOTE request `%s`: %s', mode, commands)

        ticker = ''
        currency = 'USD'
        try:
            ticker = commands[0].upper()  # should always get at least 1 command
            currency = commands[1].upper()
        except IndexError:
            pass

        try:
            raw_quote = coins.get_quote_cc([ticker], logger=logger, currency=currency)
        except Exception:
            logger.warning('COINQUOTE -- UNABLE TO GENERATE QUOTE', exc_info=True)
            return generate_platform_response(
                bot_fail_message('Can\'t resolve \'{}\''.format(commands), mode),
                mode
            )

        message = '{coin_name} {coin_price} {change_pct:+.2%} ({exchange})'.format(
            coin_name=raw_quote.loc[0, 'FullName'],
            coin_price=raw_quote.loc[0, 'PRICE'],
            change_pct=raw_quote.loc[0, 'CHANGEPCT24HOUR']/100,
            exchange=raw_quote.loc[0, 'LASTMARKET']
        )
        logger.info('quote: `%s`', message)

        return generate_platform_response(message, mode, do_code=True)
