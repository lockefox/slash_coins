"""wheel setup for slash-coins"""
from codecs import open
import importlib
from os import path, listdir

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

HERE = path.abspath(path.dirname(__file__))
__package_name__ = 'slash-coins'
__library_name__ = 'slash_coins'

def get_version(package_name):
    """find __version__ for making package

    Args:
        package_path (str): path to _version.py folder (abspath > relpath)

    Returns:
        (str) __version__ value

    """
    module = package_name + '._version'
    package = importlib.import_module(module)

    version = package.__version__

    return version

def include_all_subfiles(*args):
    """Slurps up all files in a directory (non recursive) for data_files section

    Note:
        Not recursive, only includes flat files

    Returns:
        (:obj:`list` :obj:`str`) list of all non-directories in a file

    """
    file_list = []
    for path_included in args:
        local_path = path.join(HERE, path_included)

        for file in listdir(local_path):
            file_abspath = path.join(local_path, file)
            if path.isdir(file_abspath):    #do not include sub folders
                continue
            file_list.append(path_included + '/' + file)

    return file_list

class PyTest(TestCommand):
    """PyTest cmdclass hook for test-at-buildtime functionality

    http://doc.pytest.org/en/latest/goodpractices.html#manual-integration

    """
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            'tests',
            '-rx',
            '--cov=' + __library_name__,
            '--cov-report=term-missing',
            '--cov-config=.coveragerc'
        ]    #load defaults here

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest_commands = []
        try:    #read commandline
            pytest_commands = shlex.split(self.pytest_args)
        except AttributeError:  #use defaults
            pytest_commands = self.pytest_args
        errno = pytest.main(pytest_commands)
        exit(errno)

with open('README.rst', 'r', 'utf-8') as f:
    README = f.read()


setup(
    name=__package_name__,
    description='HipChat /command REST API For CryptoCoin Quotes',
    version=get_version(__library_name__),
    long_description=README,
    author='John Purcell',
    author_email='jpurcell.ee@gmail.com',
    url='https://github.com/lockefox/' + __package_name__,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='prosper flask rest hipchat cryptocurrency integration',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('docs', include_all_subfiles('docs')),
        #('scripts'), include_all_subfiles('scripts'),
    ],
    package_data={
        '': ['LICENSE', 'README.rst', 'changelog'],
        'slash_coins': ['version.txt', 'app.cfg']
    },
    entry_points={
        'console_scripts': [
            'slash_coin_launcher=slash_coins.flask_launcher:run_main'
        ]
    },
    install_requires=[
        'ProsperCommon==1.3.0a0',
        'ProsperDatareader>=2.0.0',
        'Flask',
        'Flask-RESTful',
        'plumbum',
        'pandas',
        'numpy',
        'requests',
    ],
    tests_require=[
        'pytest',
        'pytest_cov',
        'pytest-flask',
        'shortuuid',
        'jsonschema',
    ],
    extras_require={
        'dev':[
            'sphinx',
            'sphinxcontrib-napoleon',
        ]
    },
    cmdclass={
        'test':PyTest,
    }
)
