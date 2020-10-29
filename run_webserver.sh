export MIO_CONFIG="production"
export MIO_PORT=8000
cd $(dirname $0)
work_path=$(pwd)
nohup /opt/.pyenv/versions/3.9.0/bin/python ${work_path}/mio/pymio.pyc > www.log 2>&1 &