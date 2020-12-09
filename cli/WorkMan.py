# -*- coding: utf-8 -*-
import sys
from numba import jit


class Daemon(object):
    @jit(forceobj=True)
    def hello(self, app, kwargs):
        sys_ver = sys.version
        print("Powered by PyMio.\nPython: {}".format(sys_ver))
