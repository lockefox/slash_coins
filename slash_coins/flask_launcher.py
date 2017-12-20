"""launcher/wrapper for starting Flask"""
from os import path
import platform
import logging

from flask import Flask
from flask_restful import Api

import prosper.common.prosper_cli as p_cli
import prosper.common.prosper_logging as prosper_logging
import prosper.common.prosper_config as p_config

from . import _version
from . import endpoints

HERE = path.abspath(path.dirname(__file__))

APP = Flask(_version.PROGNAME)
API = Api(APP)
API.add_resource(endpoints.Root, '/')
API.add_resource(endpoints.Version, '/version')
API.add_resource(endpoints.CoinQuote, '/coins')

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
