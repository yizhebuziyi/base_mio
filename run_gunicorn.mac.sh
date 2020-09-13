#!/bin/bash
cd $(dirname $0)
pidfile="/tmp/${1}.pid"
gunicorn --workers=${2} mio.pymio:mWSGI --worker-class='tornado' --pid=${pidfile} --max-requests=20000 --bind=0.0.0.0:8000
