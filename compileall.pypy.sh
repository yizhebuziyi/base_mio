#!/bin/bash
find . -name "*.pyc" | xargs rm -f
python -m compileall .
cp mio/__pycache__/shell.pypy36.pyc mio/shell.pyc
cp mio/__pycache__/pymio.pypy36.pyc mio/pymio.pyc
cp mio/__pycache__/passenger_wsgi.pypy36.pyc mio/passenger_wsgi.pyc