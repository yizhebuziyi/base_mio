#!/bin/bash
PYENV_ROOT="/opt/.pyenv"
PYTHON_ROOT="$PYENV_ROOT/shims"
EXECUTION="cli.WorkMan.Daemon.do_main_cron"
export PYTHONIOENCODING=utf-8
export MIO_CONFIG="production"
cd $(dirname $0)
nohup ${PYTHON_ROOT}/python mio/shell.pyc cli exe \
  -cls=${EXECUTION} > cron.log 2>&1 &