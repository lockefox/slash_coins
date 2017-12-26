FROM revolutionsystems/python:3.6.3-wee-optimized-lto

RUN pip install git+https://github.com/lockefox/slash_coins.git@master

VOLUME /opt/slash_coins/config/

WORKDIR /opt/slash_coins/

ENTRYPOINT slash_coin_launcher -v --config=/opt/slash_coins/config/app_local.cfg