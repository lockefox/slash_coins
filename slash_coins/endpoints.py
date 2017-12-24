"""endpoints.py: REST endpoints

Working off: https://bitbucket.org/travisthetechie/pypples/src/32f79e384133b36ae6883604ce8bfd66e00a5bea/pypples/api/resources.py?at=master&fileviewer=file-view-default

"""
import logging
import platform

from flask import request
from flask_restful import Resource

import prosper.datareader.coins as coins
from . import _version
from . import exceptions
from . import utils


class Version(Resource):
    """return version information about app"""
    version_payload = {
        'version': _version.__version__,
        'app_name': _version.PROGNAME
    }
    def get(self):
        """HTTP GET behavior"""
        logger = logging.getLogger(_version.PROGNAME)  # TODO: parent class + @property
        logger.info('VERSION request')
        return self.version_payload

    def post(self):
        """HTTP POST -- respond via /command"""
        logger = logging.getLogger(_version.PROGNAME)  # TODO: parent class + @property
        # Figure out what's coming in #
        try:
            mode, commands = utils.which_platform(
                request.data, request.form, contents_required=True,logger=logger
            )
        except Exception:
            logger.warning('VERSION -- INVALID PLATFORM REQUEST', exc_info=True)
            return

        logger.info('VERSION request -- `%s`: %s', mode, commands)

        return utils.generate_platform_response(str(self.version_payload), mode)


class CoinQuote(Resource):
    """generate quote for desired cryptocoin"""
    def post(self):
        """HTTP POST behavior"""
        logger = logging.getLogger(_version.PROGNAME)  # TODO: parent class + @property
        # Figure out what's coming in #
        try:
            mode, commands = utils.which_platform(
                request.data, request.form, contents_required=True,logger=logger
            )
        except Exception:
            logger.warning('COINQUOTE -- INVALID PLATFORM REQUEST', exc_info=True)
            return

        logger.info('COINQUOTE request -- `%s`: %s', mode, commands)

        ticker = ''
        currency = 'USD'
        try:
            ticker = commands[0].upper()  # should always get at least 1 command
            currency = commands[1].upper()
        except IndexError:  # pragma: no cover
            pass

        try:
            raw_quote = coins.get_quote_cc([ticker], logger=logger, currency=currency)
        except Exception:
            logger.warning('COINQUOTE -- UNABLE TO GENERATE QUOTE', exc_info=True)
            return utils.generate_platform_response(
                utils.bot_fail_message('Can\'t resolve \'{}\''.format(commands), mode),
                mode
            )

        message = '{coin_name} {coin_price} {change_pct:+.2%} ({exchange})'.format(
            coin_name=raw_quote.loc[0, 'FullName'],
            coin_price=raw_quote.loc[0, 'PRICE'],
            change_pct=raw_quote.loc[0, 'CHANGEPCT24HOUR']/100,
            exchange=raw_quote.loc[0, 'LASTMARKET']
        )
        logger.info('quote: `%s`', message)

        return utils.generate_platform_response(message, mode, do_code=True)
