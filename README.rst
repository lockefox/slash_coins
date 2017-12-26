|Show Logo|

==========
SlashCoins
==========

|Build Status| |Coverage Status| |Docs|

A REST API for publishing quick /commands for HipChat rooms.  Feed those coinbugs up-to-date quotes for their favorite cryptocoins c/o `cryptocompare`_

Routes
======

- ``/coins``: generate a coin quote from `cryptocompare`_
- ``/version``: see current version/heath status 

Getting Started
===============

Only supports Python 3.6+

Developers
----------

.. code-block::
    
    pip install -e .
    cp scripts/app.cfg scripts/app_local.cfg
    ## fill out app secrets in scripts/app_local.cfg ##
    slash_coins debug 

Install requirements in a `virtualenv`_ and use the built-in launcher to run on ``localhost``.

Deployment
----------

.. code-block::
    
    docker build -t slash-coins -f Dockerfile .
    docker run -d -v scripts/:/opt/slash_coins/config -p 8000:8000 slash-coins

TODO: more docker information

.. _cryptocompare: cryptocompare.com/api/#introduction
.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

.. |Show Logo| image:: http://dl.eveprosper.com/podcast/logo-colour-17_sm2.png
   :target: http://eveprosper.com
.. |Build Status| image:: https://travis-ci.org/lockefox/slash_coins.svg?branch=master
    :target: https://travis-ci.org/lockefox/slash_coins
.. |Coverage Status| image:: https://coveralls.io/repos/github/lockefox/slash_coins/badge.svg?branch=master
    :target: https://coveralls.io/github/lockefox/slash_coins?branch=master
.. |Docs| image:: https://readthedocs.org/projects/slash_coins/badge/?version=latest
    :target: http://slash_coins.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status