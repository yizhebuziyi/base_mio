#!/bin/bash
cd $(dirname $0)
pidfile="/tmp/${1}.pid"
/opt/.pyenv/versions/3.6.9/bin/gunicorn -c conf.py -w ${2} mio.passenger_wsgi:app \
  -k 'tornado' --pid ${pidfile} --max-requests 20000
