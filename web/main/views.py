# -*- coding: utf-8 -*-
import sys
from flask import render_template
from . import main


@main.route('/')
def index():
    sys_ver = sys.version
    return render_template('index.html', sys_ver=sys_ver)


@main.route('/client.cfm')
def client_page():
    return render_template('client.html')
