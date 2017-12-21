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

class ChatPlatform(enum.Enum):
    """help control which platform is talking to app"""
    hipchat = 'hipchat'
    slack = 'slack'
    UNKNOWN = ''

def which_platform(request_data):
    """figure out which platform is talking to app

    Args:
        request_data (dict): POST data

    Returns:
        enum: ChatPlatform

    """
    pass

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
        try:
            args = json.loads(request.data)
        except Exception:
            args = {}

        try:
            headers = request.headers
        except Exception:
            headers = {}


        logger = logging.getLogger(_version.PROGNAME)  # TODO: parent class + @property
        logger.info('COINQUOTE request -- %s -- %s', args, headers)

        return {
            'color': 'green',
            'message': 'It\'s going to be sunny tomorrow! (yey)',
            'notify': False,
            'message_format': 'text'
        }
