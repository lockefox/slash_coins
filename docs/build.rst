===================
Building SlashCoins
===================

Only supports Python 3.5+

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
    docker run -d -v scripts/:/opt/slash_coins/cfg -p 8000:8000 slash-coins

TODO: more docker information

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
