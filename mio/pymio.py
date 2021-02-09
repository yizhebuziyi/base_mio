#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
from tornado.ioloop import IOLoop
from tornado.web import Application, FallbackHandler

root_path: str = os.path.abspath(os.path.dirname(__file__) + '/../')
sys.path.append(root_path)
from mio.sys import create_app
from mio.sys.wsgi import WSGIContainerWithThread
from config import MIO_HOST, MIO_PORT

IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
try:
    os.environ['TZ'] = os.environ.get('MIO_TIMEZONE') or 'Asia/Shanghai'
    time.tzset()
except:
    pass

index = -1
MIO_CONFIG: str = os.environ.get('MIO_CONFIG') or 'default'
MIO_APP_CONFIG: str = os.environ.get('MIO_APP_CONFIG') or 'config'
if MIO_CONFIG == 'production':
    log_level = logging.INFO
else:
    log_level = logging.DEBUG
for arg in sys.argv:
    index += 1
    if index <= 0:
        continue
    if not arg.startswith('--'):
        continue
    arg = arg[2:]
    temp = arg.split('=')
    if temp[0].lower() == 'app_config':
        MIO_APP_CONFIG: str = temp[1]
        continue
    if temp[0].lower() == 'host':
        MIO_HOST: str = temp[1]
        os.environ["MIO_HOST"] = MIO_HOST
        continue
    if temp[0].lower() == 'port':
        try:
            port: int = int(temp[1])
            MIO_PORT = port
            os.environ["MIO_PORT"] = str(MIO_PORT)
        except Exception as e:
            print(e)
            exit()
        continue
    if temp[0].lower() == 'config':
        MIO_CONFIG = temp[1]
        continue
app, wss = create_app(MIO_CONFIG, root_path, MIO_APP_CONFIG, log_level=log_level)
wss.append((r'.*', FallbackHandler, dict(fallback=WSGIContainerWithThread(app))))
mWSGI: Application = Application(wss)

if __name__ == '__main__':
    try:
        http_server: Application = mWSGI
        http_server.listen(MIO_PORT, MIO_HOST)
        print("WebServer listen in http://{}:{}".format(MIO_HOST, MIO_PORT))
        IOLoop.instance().start()
    except KeyboardInterrupt:
        print("WebServer Closed.")
