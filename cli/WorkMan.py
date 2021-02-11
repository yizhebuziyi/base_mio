# -*- coding: utf-8 -*-
# from numba import jit
import sys
from mio.util.Logs import LogHandler


class Daemon(object):
    # @jit(forceobj=True)
    def hello(self, app, kwargs):
        # sys_ver = sys.version
        # print("Powered by PyMio.\nPython: {}".format(sys_ver))
        from mio.util.mq.request_reply import Server
        s = Server(logger=LogHandler('Daemon.hello').logger)
        s.run()
        pass
