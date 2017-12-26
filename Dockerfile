FROM revolutionsystems/python:3.6.3-wee-optimized-lto

RUN pip install git+https://github.com/lockefox/slash_coins.git@master

WORKDIR /opt/slash_coins/

ENTRYPOINT slash_coin_launcher -v