#!/bin/bash
cd $(dirname $0)
pidfile="/tmp/${1}.pid"
MIO_CONFIG="production" /opt/.pyenv/versions/pypy3.6-7.3.1/bin/gunicorn -w ${2} mio.pymio:mWSGI \
  -k 'tornado' --pid ${pidfile} --max-requests 20000
