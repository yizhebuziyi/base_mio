#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

root_path = os.path.abspath(os.path.dirname(__file__) + '/../')
sys.path.append(root_path)
from mio.pymio import mWSGI
from flask_script import Manager

from mio.ext.cli import CliCommand

manager = Manager(mWSGI)
manager.add_command('cli', CliCommand)

if __name__ == '__main__':
    manager.run()
