===================
Building SlashCoins
===================

Only supports Python 3.6+.  Designed to respond seemlessly to both HipChat & Slack requests.

Direct Install
--------------

.. code-block::
    
    pip install -e .
    slash_coin_launcher -v -d

Install requirements in a `virtualenv`_ and use the built-in launcher to run on ``localhost``.  Launch without ``-d/--debug`` for production mode.  

Also, for configurations, ``slash_coin_launcher --dump-config > app_local.cfg`` will allow you to write secrets to a config file.  Then just launch with ``slash_coin_launcher --config=path/to/app_local.cfg``.  

Dockerfile
----------

Tools have been included to deploy your own via Docker!  Built off `Optimized Python`_ Docker image.

.. code-block::
    
    docker build -t slash-coins -f Dockerfile .
    docker run -d -p 8000:8000 slash-coins

Customize with docker ENV flags

- ``PROSPER_LOGGING__discord_webhook``: log error messages to Discord
- ``PROSPER_LOGGING__slack_webhook``: log error messages to Slack
- ``PROSPER_LOGGING__hipchat_webhook``: log error messages to HipChat 
- ``PROSPER_FLASK__port``: change outgoing Flask port

PythonAnywhere
--------------

`PythonAnywhere`_ is an amazing resource for hacker projects, and makes it easy to piggyback off their HTTPS certs rather than rolling your own for HipChat compliance.

Instructions based off their `webapp launch guide`_.  Follow instructions to pip-install project, then add this to the WSGI config. 

.. code-block:: python
    :caption: /var/www/{username}_pythonanywhere_com_wsgi.py

    ...
    # import flask app but need to call it "application" for WSGI to work
    from slash_coins.flask_launcher import build_logger_pythonanywhere
    build_logger_pythonanywhere(
        '/home/lockefox/slash_coins/slash_coins/app_local.cfg',
        debug=True
    )

    from slash_coins.flask_launcher import APP as application

Because slash_coins has `ProsperCommon`_ logging built in, we need to add our logger into the logging tree.  Also, the names are changed slightly to be more PEP8.  


.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
.. _Optimized Python: https://www.revsys.com/tidbits/optimized-python/
.. _PythonAnywhere: https://www.pythonanywhere.com
.. _webapp launch guide: https://help.pythonanywhere.com/pages/Flask/
.. _ProsperCommon: http://prospercommon.readthedocs.io/en/latest/
