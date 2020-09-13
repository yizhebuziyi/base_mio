#!/bin/bash
find . -name "*.pyc" | xargs rm -f
python -m compileall .
cp mio/__pycache__/shell.cpython-36.pyc mio/shell.pyc
cp mio/__pycache__/pymio.cpython-36.pyc mio/pymio.pyc