#!/bin/bash
export MIO_CONFIG="production"
export MIO_PORT=8000
PYENV_ROOT="/usr/local/.pyenv"
PYTHON_ROOT="$PYENV_ROOT/shims"
export PYTHONIOENCODING=utf-8
export MIO_CONFIG="production"
export MIO_LIMIT_CPU=1
cd $(dirname $0)
work_path=$(pwd)
mkdir -p "${work_path}/logs"
ulimit -n 512000
#nohup ${PYTHON_ROOT}/python "${work_path}/mio/pymio.pyc" > "${work_path}/logs/www.log" 2>&1 &
${PYTHON_ROOT}/python -u "${work_path}/mio/pymio.pyc" > "${work_path}/logs/www.log" 2>&1