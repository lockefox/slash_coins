FROM revolutionsystems/python:3.6.3-wee-optimized-lto

RUN pip install git+https://github.com/lockefox/slash_coins.git@master

VOLUME /opt/slash_coins/config

ENTRYPOINT slash_coin_launcher --config=/opt/slash_coins/config/app.config