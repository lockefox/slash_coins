"""test_launcher: make sure flask_launcher does its job"""
from plumbum import local

import slash_coins._version as _version
COMMAND_NAME = 'slash_coin_launcher'
class TestCLI:
    """validate flask_launcher works as expected"""
    app_command = local[COMMAND_NAME]

    def test_help(self):
        """validate -h works"""
        output = self.app_command('-h')

    def test_version(self):
        """validate app name/version are as expected"""
        output = self.app_command('--version')

        assert output.strip() == '{app_name} {version}'.format(
            app_name=_version.PROGNAME,
            version=_version.__version__
        )
