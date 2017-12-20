"""launcher/wrapper for starting Flask"""
from os import path
import platform

import prosper.common.prosper_cli as p_cli
import prosper.common.prosper_logging as prosper_logging
import prosper.common.prosper_config as p_config

from . import _version

HERE = path.abspath(path.dirname(__file__))


class FlaskLauncher(p_cli.ProsperApplication):
    PROGNAME = _version.PROGNAME
    VERSION = _version.__version__

    config_path = path.join(HERE, 'app.config')

    def main(self):
        """launcher logic"""
        self.logger.info('hello world')

def run_main():
    """entry point for launching app"""
    FlaskLauncher.run()

if __name__ == '__main__':
    run_main()
