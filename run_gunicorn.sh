#!/bin/bash
export MIO_CONFIG="production"
export MIO_PORT=8000
PYENV_ROOT="/usr/local/.pyenv"
PYTHON_ROOT="$PYENV_ROOT/versions/3.9.1/bin"
cd $(dirname $0)
pidfile="/tmp/${1}.pid"
${PYTHON_ROOT}/gunicorn --workers=${2} mio.pymio:mWSGI \
  --worker-class='tornado' --pid=${pidfile} --max-requests=20000
