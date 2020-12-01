#!/bin/bash
find . -name "*.pyc" | xargs rm -f
python -m compileall .
cp mio/__pycache__/shell.cpython-39.pyc mio/shell.pyc
cp mio/__pycache__/pymio.cpython-39.pyc mio/pymio.pyc