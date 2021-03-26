export MIO_CONFIG="production"
export MIO_PORT=8000
PYENV_ROOT="/usr/local/.pyenv"
PYTHON_ROOT="$PYENV_ROOT/shims"
export PYTHONIOENCODING=utf-8
export MIO_CONFIG="production"
export MIO_LIMIT_CPU=1
cd $(dirname $0)
work_path=$(pwd)
nohup ${PYTHON_ROOT}/python ${work_path}/mio/pymio.pyc > www.log 2>&1 &