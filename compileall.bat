@echo off
python\python -m compileall -f .
move mio\__pycache__\shell.cpython-39.pyc mio\shell.pyc
move mio\__pycache__\pymio.cpython-39.pyc mio\pymio.pyc