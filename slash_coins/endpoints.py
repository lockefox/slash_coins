"""endpoints.py: REST endpoints

Working off: https://bitbucket.org/travisthetechie/pypples/src/32f79e384133b36ae6883604ce8bfd66e00a5bea/pypples/api/resources.py?at=master&fileviewer=file-view-default

"""
import logging
import json

from flask import request
from flask_restful import Resource

import prosper.datareader.coins as coins
from . import _version

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

class CoinQuote(Resource):
    """generate quote for desired cryptocoin"""
    def post(self):
        """HTTP POST behavior"""
        args = json.loads(request.data)
        logger = logging.getLogger(_version.PROGNAME)  # TODO: parent class + @property
        logger.info('COINQUOTE request -- %s', args)

