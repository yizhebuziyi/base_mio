# -*- coding: utf-8 -*-
import os
import sys

os.environ["MIO_CONFIG"] = 'production'
root_path = os.path.abspath(os.path.dirname(__file__) + '/../')
sys.path.append(root_path)
from mio.pymio import app, socket_io
