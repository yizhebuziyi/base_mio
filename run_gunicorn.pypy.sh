#!/bin/bash
cd $(dirname $0)
pidfile="/tmp/${1}.pid"
/opt/.pyenv/versions/pypy3.6-7.3.1/bin/gunicorn -c conf.py -w ${2} mio.passenger_wsgi:app \
  -k 'tornado' --pid ${pidfile} --max-requests 20000
