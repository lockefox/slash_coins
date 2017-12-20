"""launcher/wrapper for starting Flask"""
from os import path
import platform
import logging

from flask import Flask
from flask_restful import Api

import prosper.common.prosper_cli as p_cli
import prosper.common.prosper_logging as p_logging
import prosper.common.prosper_config as p_config

from . import _version
from . import endpoints

HERE = path.abspath(path.dirname(__file__))

APP = Flask(_version.PROGNAME)
API = Api(APP)
API.add_resource(endpoints.Root, '/')
API.add_resource(endpoints.Version, '/version')
API.add_resource(endpoints.CoinQuote, '/coins')

def build_logger_pythonanywhere(
        config_path,
        log_name=_version.PROGNAME,
        debug=False
):
    """build a logger outside the CLI FlaskLauncher

    Args:
        config_path (str): path to config file
        log_name (str): name of log
        debug (bool): enable stdout loggers and disable webhook loggers

    """
    config = p_config.ProsperConfig(config_path)
    builder = p_logging.ProsperLogger(
        log_name,
        config.get('LOGGING', 'log_path'),
        config_obj=config
    )

    if debug:
        builder.configure_debug_logger()
    else:
        if config.get('LOGGING', 'discord_webhook'):
            builder.configure_discord_logger()
        if config.get('LOGGING', 'slack_webhook'):
            builder.configure_slack_logger()
        if config.get('LOGGING', 'hipchat_webhook'):
            builder.configure_hipchat_logger()

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
