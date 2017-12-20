"""__init__.py: Flask app configuration"""
import warnings
import logging

try:
    from flask import Flask
except ImportError:
    warnings.warn('pre-install mode -- requirements not installed', UserWarning)

def create_app(
        settings=None,
        config=None,
        testmode=False
):
    """create Flask application

    Args:
        settings (:obj:`dict`): Flask settings
        config (:obj:`configparser.ConfigParser`): specific app configs
        testmode (bool): run without prod modes

    Returns:
        flask.app

    """
    pass
