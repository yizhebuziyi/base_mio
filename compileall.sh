#!/bin/bash
find . -name "*.pyc" | xargs rm -f
python -m compileall .
cp mio/__pycache__/shell.cpython-38.pyc mio/shell.pyc
cp mio/__pycache__/pymio.cpython-38.pyc mio/pymio.pyc