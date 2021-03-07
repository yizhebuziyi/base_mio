# -*- coding: utf-8 -*-
import tornado
from tornado import escape
from tornado import httputil
from tornado.httputil import ResponseStartLine, HTTPHeaders
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
# from numba import jit
from typing import List, Tuple, Optional, Callable, Any, Type
from types import TracebackType

MIO_SYSTEM_VERSION = '1.3.0'


class WSGIContainerWithThread(WSGIContainer):
    @tornado.gen.coroutine
    def __call__(self, request):
        data = {}
        response: List[bytes] = []

        # @jit(forceobj=True, parallel=True)
        def start_response(
                status: str,
                headers: List[Tuple[str, str]],
                exec_info: Optional[
                    Tuple[
                        Optional[Type[BaseException]],
                        Optional[BaseException],
                        Optional[TracebackType],
                    ]
                ] = None,
        ) -> Callable[[bytes], Any]:
            data['status'] = status
            data['headers'] = headers
            return response.append

        IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
        loop = IOLoop.instance()

        app_response = yield loop.run_in_executor(None, self.wsgi_application,
                                                  WSGIContainer.environ(request),
                                                  start_response)
        try:
            response.extend(app_response)
            body: bytes = b''.join(response)
        finally:
            if hasattr(app_response, 'close'):
                app_response.close()
        if not data:
            raise Exception('WSGI app did not call start_response')
        status_code_str, reason = str(data['status']).split(' ', 1)
        status_code: int = int(status_code_str)
        headers: List[tuple] = data['headers']
        header_set = set(k.lower() for (k, v) in headers)
        body = escape.utf8(body)
        if status_code != 304:
            if 'content-length' not in header_set:
                headers.append(('Content-Length', str(len(body))))
            if 'content-type' not in header_set:
                headers.append(('Content-Type', 'text/html; charset=UTF-8'))
        if 'server' not in header_set:
            headers.append(('Server', 'PyMio/{}'.format(MIO_SYSTEM_VERSION)))
        start_line: ResponseStartLine = httputil.ResponseStartLine('HTTP/1.1', status_code, reason)
        header_obj: HTTPHeaders = httputil.HTTPHeaders()
        for key, value in headers:
            header_obj.add(key, value)
        assert request.connection is not None
        request.connection.write_headers(start_line, header_obj, chunk=body)
        request.connection.finish()
        self._log(status_code, request)
