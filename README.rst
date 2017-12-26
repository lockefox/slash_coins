|Show Logo|

==========
SlashCoins
==========

|Build Status| |Coverage Status| |Docs|

A REST API for publishing quick /commands for HipChat and Slack rooms.  Feed those coinbugs up-to-date quotes for their favorite cryptocoins c/o `cryptocompare`_

Want to use it right now?  Point your integration at:

    https://lockefox.pythonanywhere.com/coins

    Then use ``/command COINTICKER CURRENCY[optional]``

Deploy Your Own
===============

Tools have been included to deploy your own via Docker!

.. code-block::
    
    docker build -t slash-coins -f Dockerfile .
    docker run -d -p 8000:8000 slash-coins

Customize with docker ENV flags

- ``PROSPER_LOGGING__discord_webhook``: log error messages to Discord
- ``PROSPER_LOGGING__slack_webhook``: log error messages to Slack
- ``PROSPER_LOGGING__hipchat_webhook``: log error messages to HipChat 
- ``PROSPER_FLASK__port``: change outgoing Flask port

Routes
======

- ``/coins``: generate a coin quote from `cryptocompare`_
- ``/version``: see current version/heath status 

For Developers
==============

Only supports Python 3.6+

.. code-block::
    
    pip install -e .
    cp slash_coins/app.cfg slash_coins/app_local.cfg
    ## fill out app secrets in slash_coins/app_local.cfg ##
    slash_coin_launcher -v -d --config=slash_coins/app_local.cfg

Install requirements in a `virtualenv`_ and use the built-in launcher to run on ``localhost``.


.. _cryptocompare: cryptocompare.com/api/#introduction
.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

.. |Show Logo| image:: http://dl.eveprosper.com/podcast/logo-colour-17_sm2.png
   :target: http://eveprosper.com
.. |Build Status| image:: https://travis-ci.org/lockefox/slash_coins.svg?branch=master
    :target: https://travis-ci.org/lockefox/slash_coins
.. |Coverage Status| image:: https://coveralls.io/repos/github/lockefox/slash_coins/badge.svg?branch=master
    :target: https://coveralls.io/github/lockefox/slash_coins?branch=master
.. |Docs| image:: https://readthedocs.org/projects/slash-coins/badge/?version=latest
:target: http://slash-coins.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status
