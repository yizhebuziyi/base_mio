#!/bin/bash
PYENV_ROOT="/usr/local/.pyenv"
PYTHON_ROOT="$PYENV_ROOT/shims"
cd $(dirname $0)
${PYTHON_ROOT}/pip install -U -r requirements.txt
bash compileall.sh
#work_path=$(pwd)
${PYTHON_ROOT}/circusd --daemon circus.ini
#circusd circus.ini