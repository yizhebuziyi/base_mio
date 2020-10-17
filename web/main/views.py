# -*- coding: utf-8 -*-
import os
import sys
from flask import send_from_directory, render_template
from mio.util.Helper import get_root_path
from . import main


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(get_root_path(), 'web', 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@main.route('/')
def index():
    sys_ver = sys.version
    return render_template('index.html', sys_ver=sys_ver)


@main.route('/client.cfm')
def client_page():
    return render_template('client.html')
