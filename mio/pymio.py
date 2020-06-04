#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

root_path = os.path.abspath(os.path.dirname(__file__) + '/../')
sys.path.append(root_path)
from mio.sys import create_app, socket_io
from config import MIO_HOST, MIO_PORT

index = -1
MIO_CONFIG = os.environ.get('MIO_CONFIG') or 'default'
MIO_APP_CONFIG = os.environ.get('MIO_APP_CONFIG') or 'config'
for arg in sys.argv:
    index += 1
    if index <= 0:
        continue
    if not arg.startswith('--'):
        continue
    arg = arg[2:]
    temp = arg.split('=')
    if temp[0].lower() == 'app_config':
        MIO_APP_CONFIG = temp[1]
        continue
    if temp[0].lower() == 'host':
        MIO_HOST = temp[1]
        os.environ["MIO_HOST"] = MIO_HOST
        continue
    if temp[0].lower() == 'port':
        try:
            port = int(temp[1])
            MIO_PORT = port
            os.environ["MIO_PORT"] = str(MIO_PORT)
        except Exception as e:
            print(e)
            exit()
        continue
    if temp[0].lower() == 'config':
        MIO_CONFIG = temp[1]
        continue
app = create_app(MIO_CONFIG, root_path, MIO_APP_CONFIG)

if __name__ == '__main__':
    try:
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(MIO_PORT, MIO_HOST)
        print("WebServer listen in http://{}:{}".format(MIO_HOST, MIO_PORT))
        IOLoop.instance().start()
    except KeyboardInterrupt:
        print("WebServer Closed.")
