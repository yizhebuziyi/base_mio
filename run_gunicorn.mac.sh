#!/bin/bash
cd $(dirname $0)
pidfile="/tmp/${1}.pid"
gunicorn -w ${2} mio.pymio:mWSGI -k 'tornado' --pid ${pidfile} --max-requests 20000
