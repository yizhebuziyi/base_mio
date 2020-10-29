#!/bin/bash
cd $(dirname $0)
pidfile="/tmp/${1}.pid"
MIO_CONFIG="production" /opt/.pyenv/versions/3.9.0/bin/gunicorn --workers=${2} mio.pymio:mWSGI \
  --worker-class='tornado' --pid=${pidfile} --max-requests=20000
