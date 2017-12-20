"""launcher/wrapper for starting Flask"""
from os import path
import platform
import logging

from flask import Flask, jsonify

import prosper.datareader.coins as coins
import prosper.common.prosper_cli as p_cli
import prosper.common.prosper_logging as prosper_logging
import prosper.common.prosper_config as p_config

from . import _version

HERE = path.abspath(path.dirname(__file__))

APP = Flask(_version.PROGNAME)

@APP.route('/version')
def version_endpoint():
    """respond with current version information"""
    logger = logging.getLogger(_version.PROGNAME)
    logger.info('Version Endpoint:')#' %s', payload)
    return jsonify(
        version=_version.__version__,
        app_name=_version.PROGNAME
    )

@APP.route('/quote/<payload>')
def quote_endpoint(payload):
    """respond with quote for cryptocoin"""
    logger = logging.getLogger(_version.PROGNAME)
    logger.info('Quote Endpoint: %s', payload)
    return {'hello': 'world'}


class FlaskLauncher(p_cli.ProsperApplication):
    PROGNAME = _version.PROGNAME
    VERSION = _version.__version__

    config_path = path.join(HERE, 'app.cfg')

    def main(self):
        """launcher logic"""
        self.logger.info('hello world')

        try:
            if self.debug:
                self.logger.warning('LAUNCHING %s -- %s -- DEBUG', self.PROGNAME, platform.node())
                APP.run(
                    host='127.0.0.1',
                    port=int(self.config.get('FLASK', 'port')),
                    debug=True
                )
            else:
                self.logger.error('LAUNCHING %s -- %s', self.PROGNAME, platform.node())
                APP.run(
                    host='0.0.0.0',
                    port=int(self.config.get('FLASK', 'port')),
                )
        except Exception:
            self.logger.critical('%s GOING DOWN IN FLAMES!', exc_info=True)

def run_main():
    """entry point for launching app"""
    FlaskLauncher.run()

if __name__ == '__main__':
    run_main()
