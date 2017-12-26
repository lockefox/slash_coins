.. SlashCoins documentation master file, created by
   sphinx-quickstart on Tue Dec 19 16:57:42 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==========
SlashCoins
==========

|Build Status| |Coverage Status| |Docs|

A REST API for publishing quick /commands for HipChat & Slack rooms.  Feed your coinbugs up-to-date quotes for their favorite cryptocoins c/o `cryptocompare`_

Try it now!  Point your /command integration at: 
    
    https://lockefox.pythonanywhere.com/coins

Then ``/[command] COINTICKER CURRENCY(optional)`` should yield the latest quote for your favorite cryptocoin.

Deploy Your Own
===============

Easy to deploy in a couple different ways.  See `build`_ documentation for details.

- Direct install: ``slash_coin_launcher`` 
- Dockerfile
- PythonAnywhere 

Index
=====

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    build.rst

.. _cryptocompare: cryptocompare.com/api/#introduction
.. _build: build.html

.. |Show Logo| image:: http://dl.eveprosper.com/podcast/logo-colour-17_sm2.png
   :target: http://eveprosper.com
.. |Build Status| image:: https://travis-ci.org/lockefox/slash_coins.svg?branch=master
    :target: https://travis-ci.org/lockefox/slash_coins
.. |Coverage Status| image:: https://coveralls.io/repos/github/lockefox/slash_coins/badge.svg?branch=master
    :target: https://coveralls.io/github/lockefox/slash_coins?branch=master
.. |Docs| image:: https://readthedocs.org/projects/slash-coins/badge/?version=latest
    :target: http://slash-coins.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status