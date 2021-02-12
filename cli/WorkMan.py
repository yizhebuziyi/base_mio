# -*- coding: utf-8 -*-
# from numba import jit
import sys


class Daemon(object):
    # @jit(forceobj=True)
    def hello(self, app, kwargs):
        sys_ver = sys.version
        print("Powered by PyMio.\nPython: {}".format(sys_ver))
        pass
