"""endpoints.py: REST endpoints

Working off: https://bitbucket.org/travisthetechie/pypples/src/32f79e384133b36ae6883604ce8bfd66e00a5bea/pypples/api/resources.py?at=master&fileviewer=file-view-default

"""
import logging
import platform

from flask import request
from flask_restful import Resource

import prosper.datareader.coins as coins
import prosper.datareader.stocks as stocks
import prosper.datareader.news as news
import prosper.datareader.utils as pdr_utils
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
                request.data, request.form, contents_required=True, logger=logger
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

class StockQuote(Resource):
    """generate quote and news article for stock"""
    def post(self):
        """HTTP POST behavior"""
        logger = logging.getLogger(_version.PROGNAME)
        try:
            mode, commands = utils.which_platform(
                request.data, request.form, contents_required=True, logger=logger
            )
        except Exception:
            logger.warning('STOCKQUOTE -- INVALID PLATFORM REQUEST', exc_info=True)
            return

        try:
            ticker = commands[0].upper()
            quote_df = stocks.get_quote_rh(ticker)
            news_df = news.company_headlines_yahoo(ticker)
            news_df = pdr_utils.vader_sentiment(news_df, 'title', logger=logger)
        except Exception:
            logger.warning('STOCKQUOTE -- unable to get quote/news `%s`', ticker, exc_info=True)
            return utils.generate_platform_response(
                utils.bot_fail_message('Can\'t resolve \'{}\''.format(commands), mode),
                mode
            )

        direction = float(quote_df.iloc[0]['change_pct'].replace('%', ''))
        url = ''
        score = 0.0
        if direction > 0:  # pragma: no cover
            logger.info('--parsing positive news')
            best_article = news_df[news_df['compound'] == max(news_df['compound'])]
            url = best_article.iloc[0]['link']
            score = best_article.iloc[0]['compound']
        elif direction < 0:  # pragma: no cover
            logger.info('--parsing negative news')
            best_article = news_df[news_df['compound'] == min(news_df['compound'])]
            url = best_article.iloc[0]['link']
            score = best_article.iloc[0]['compound']
        else:  # pragma: no cover
            logger.warning('--neutral news -- unsupported')

        logger.debug('%s -- %s', score, url)


        return utils.generate_platform_response(
            '{} \n {} ({})'.format(' '.join(list(map(str, quote_df.iloc[0]))), url, score),
            mode
        )
