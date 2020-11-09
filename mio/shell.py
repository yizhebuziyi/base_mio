#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

root_path = os.path.abspath(os.path.dirname(__file__) + '/../')
sys.path.append(root_path)
from mio.pymio import app
from flask_script import Manager

from mio.ext.cli import CliCommand

manager = Manager(app)
manager.add_command('cli', CliCommand)
if app.config['RMDB_SYS_ENABLE']:
    from mio.sys import rmdb
    from flask_migrate import Migrate, MigrateCommand

    migrate = Migrate(app=app, db=rmdb)
    manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
