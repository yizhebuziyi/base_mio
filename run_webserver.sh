export MIO_CONFIG="production"
export MIO_PORT=8000
PYENV_ROOT="/usr/local/.pyenv"
PYTHON_ROOT="$PYENV_ROOT/shims"
cd $(dirname $0)
work_path=$(pwd)
nohup ${PYTHON_ROOT}/python ${work_path}/mio/pymio.pyc > www.log 2>&1 &