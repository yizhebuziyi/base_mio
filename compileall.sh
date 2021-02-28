#!/bin/bash
find . -name "*.pyc" | xargs rm -f
python -m compileall .
python pack.py