@echo off
python\python -m compileall -f .
move mio\__pycache__\shell.cpython-36.pyc mio\shell.pyc
move mio\__pycache__\pymio.cpython-36.pyc mio\pymio.pyc