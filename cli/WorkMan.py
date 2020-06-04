# -*- coding: utf-8 -*-
import sys


class Daemon(object):
    def hello(self, app, kwargs):
        sys_ver = sys.version
        print("Powered by PyMio.\nPython: {}".format(sys_ver))
