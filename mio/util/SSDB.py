# -*- coding: utf-8 -*-
import os, sys
from sys import stdin, stdout

import socket


class SSDB_Response(object):
    def __init__(self, code='', data_or_message=None):
        self.type = 'none'
        self.code = code
        self.data = None
        self.message = None
        self.set(code, data_or_message)

    def set(self, code, data_or_message=None):
        self.code = code

        if code == 'ok':
            self.data = data_or_message
        else:
            if isinstance(data_or_message, list):
                if len(data_or_message) > 0:
                    self.message = data_or_message[0]
            else:
                pass
                self.message = data_or_message

    def __repr__(self):
        return (((str(self.code) + ' ') + str(self.message)) + ' ') + str(self.data)

    def ok(self):
        return self.code == 'ok'

    def not_found(self):
        return self.code == 'not_found'

    def str_resp(self, resp):
        self.type = 'val'

        if resp[0] == 'ok':
            if len(resp) == 2:
                self.set('ok', resp[1])
            else:
                self.set('server_error', 'Invalid response')
        else:
            self.set(resp[0], resp[1:])
        return self

    def str_resp(self, resp):
        self.type = 'val'

        if resp[0] == 'ok':
            if len(resp) == 2:
                self.set('ok', resp[1])
            else:
                self.set('server_error', 'Invalid response')
        else:
            self.set(resp[0], resp[1:])
        return self

    def int_resp(self, resp):
        self.type = 'val'

        if resp[0] == 'ok':
            if len(resp) == 2:
                try:
                    val = int(resp[1])
                    self.set('ok', val)
                except Exception as e:
                    self.set('server_error', str(e))
            else:
                self.set('server_error', 'Invalid response')
        else:
            self.set(resp[0], resp[1:])
        return self

    def float_resp(self, resp):
        self.type = 'val'

        if resp[0] == 'ok':
            if len(resp) == 2:
                try:
                    val = float(resp[1])
                    self.set('ok', val)
                except Exception as e:
                    self.set('server_error', set(e))
            else:
                self.set('server_error', 'Invalid response')
        else:
            self.set(resp[0], resp[1:])
        return self

    def list_resp(self, resp):
        self.type = 'list'
        self.set(resp[0], resp[1:])
        return self

    def int_map_resp(self, resp):
        self.type = 'map'

        if resp[0] == 'ok':
            if len(resp) % 2 == 1:
                pass
                data = {'index': [], 'items': {}, }
                i = 1

                while i < len(resp):
                    pass
                    k = resp[i]
                    v = resp[(i + 1)]
                    try:
                        pass
                        v = int(v)
                    except Exception as e:
                        str(e)
                        v = -1
                    data['index'].append(k)
                    data['items'][k] = v
                    i += 2
                self.set('ok', data)
            else:
                self.set('server_error', 'Invalid response')
        else:
            self.set(resp[0], resp[1:])
        return self

    def str_map_resp(self, resp):
        self.type = 'map'

        if resp[0] == 'ok':
            if len(resp) % 2 == 1:
                data = {'index': [], 'items': {}, }
                i = 1

                while i < len(resp):
                    k = resp[i]
                    v = resp[(i + 1)]
                    data['index'].append(k)
                    data['items'][k] = v
                    i += 2
                self.set('ok', data)
            else:
                self.set('server_error', 'Invalid response')
        else:
            self.set(resp[0], resp[1:])
        return self


class SSDB(object):
    def __init__(self, host, port):
        self.recv_buf = ''
        self._closed = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(tuple([host, port]))
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    def close(self):
        if not self._closed:
            self.sock.close()
            self._closed = True

    def closed(self):
        return self._closed

    def request(self, cmd, params=None):
        if params is None:
            params = []
        params = ([cmd] + params)
        self.send(params)
        resp = self.recv()

        if resp is None:
            return SSDB_Response('error', 'Unknown error')

        if len(resp) == 0:
            return SSDB_Response('disconnected', 'Connection closed')
        ret = SSDB_Response()

        # {{{ switch: cmd
        while True:
            if False or (cmd == 'ping') or (cmd == 'set') or (cmd == 'del') or (cmd == 'qset') or (
                    cmd == 'zset') or (cmd == 'hset') or (cmd == 'qpush') or (cmd == 'qpush_front') or (
                    cmd == 'qpush_back') or (cmd == 'zdel') or (cmd == 'hdel') or (cmd == 'multi_set') or (
                    cmd == 'multi_del') or (cmd == 'multi_hset') or (cmd == 'multi_hdel') or (
                    cmd == 'multi_zset') or (cmd == 'multi_zdel'):
                if len(resp) > 1:
                    return ret.int_resp(resp)
                else:
                    return SSDB_Response(resp[0], None)
            if False or (cmd == 'version') or (cmd == 'substr') or (cmd == 'get') or (cmd == 'getset') or (
                    cmd == 'hget') or (cmd == 'qfront') or (cmd == 'qback') or (cmd == 'qget'):
                return ret.str_resp(resp)
            if False or (cmd == 'qpop') or (cmd == 'qpop_front') or (cmd == 'qpop_back'):
                size = 1
                try:
                    size = int(params[2])
                except Exception as e:
                    str(e)

                if size == 1:
                    return ret.str_resp(resp)
                else:
                    return ret.list_resp(resp)
            if False or (cmd == 'dbsize') or (cmd == 'getbit') or (cmd == 'setbit') or (cmd == 'countbit') or (
                    cmd == 'bitcount') or (cmd == 'strlen') or (cmd == 'ttl') or (cmd == 'expire') or (
                    cmd == 'setnx') or (cmd == 'incr') or (cmd == 'decr') or (cmd == 'zincr') or (
                    cmd == 'zdecr') or (cmd == 'hincr') or (cmd == 'hdecr') or (cmd == 'hsize') or (
                    cmd == 'zsize') or (cmd == 'qsize') or (cmd == 'zget') or (cmd == 'zrank') or (
                    cmd == 'zrrank') or (cmd == 'zsum') or (cmd == 'zcount') or (cmd == 'zremrangebyrank') or (
                    cmd == 'zremrangebyscore') or (cmd == 'hclear') or (cmd == 'zclear') or (
                    cmd == 'qclear') or (cmd == 'qpush') or (cmd == 'qpush_front') or (cmd == 'qpush_back') or (
                    cmd == 'qtrim_front') or (cmd == 'qtrim_back'):
                return ret.int_resp(resp)
            if False or (cmd == 'zavg'):
                return ret.float_resp(resp)
            if False or (cmd == 'keys') or (cmd == 'rkeys') or (cmd == 'zkeys') or (cmd == 'zrkeys') or (
                    cmd == 'hkeys') or (cmd == 'hrkeys') or (cmd == 'list') or (cmd == 'hlist') or (
                    cmd == 'hrlist') or (cmd == 'zlist') or (cmd == 'zrlist'):
                return ret.list_resp(resp)
            if False or (cmd == 'scan') or (cmd == 'rscan') or (cmd == 'hgetall') or (cmd == 'hscan') or (
                    cmd == 'hrscan'):
                return ret.str_map_resp(resp)
            if False or (cmd == 'zscan') or (cmd == 'zrscan') or (cmd == 'zrange') or (cmd == 'zrrange') or (
                    cmd == 'zpop_front') or (cmd == 'zpop_back'):
                return ret.int_map_resp(resp)
            if False or (cmd == 'auth') or (cmd == 'exists') or (cmd == 'hexists') or (cmd == 'zexists'):
                return ret.int_resp(resp)
            if False or (cmd == 'multi_exists') or (cmd == 'multi_hexists') or (cmd == 'multi_zexists'):
                return ret.int_map_resp(resp)
            if False or (cmd == 'multi_get') or (cmd == 'multi_hget'):
                return ret.str_map_resp(resp)
            if False or (cmd == 'multi_hsize') or (cmd == 'multi_zsize') or (cmd == 'multi_zget'):
                return ret.int_map_resp(resp)
            ### default
            return ret.list_resp(resp)
        # }}} switch

    def send(self, data):
        ps = []

        _cpy_r_0 = _cpy_l_1 = data
        if type(_cpy_r_0).__name__ == 'dict':
            _cpy_b_3 = True
            _cpy_l_1 = _cpy_r_0.iterkeys()
        else:
            _cpy_b_3 = False
        for _cpy_k_2 in _cpy_l_1:
            if _cpy_b_3:
                p = _cpy_r_0[_cpy_k_2]
            else:
                p = _cpy_k_2
            p = str(p)
            ps.append(str(len(p)))
            ps.append(p)
        nl = '\n'
        s = (nl.join(ps) + '\n\n')
        try:
            while True:
                ret = self.sock.send(s.encode('utf-8'))

                if ret == 0:
                    return -1
                s = s[ret:]

                if len(s) == 0:
                    break
        except socket.error as e:
            str(e)
            return -1
        return ret

    def net_read(self):
        try:
            data = self.sock.recv(1024 * 8)
        except Exception as e:
            str(e)
            data = ''

        if data is None or data == '':
            self.close()
            return 0
        data = data.decode('utf-8') if isinstance(data, bytes) else data
        self.recv_buf += data
        return len(data)

    def recv(self):
        while True:
            ret = self.parse()

            if ret is None:
                if self.net_read() == 0:
                    return []
            else:
                return ret

    def parse(self):
        ret = []
        spos = 0
        epos = 0

        while True:
            spos = epos
            epos = self.recv_buf.find('\n', spos)

            if epos == -1:
                break
            epos += 1
            line = self.recv_buf[spos: epos]
            spos = epos

            if line.strip() == '':
                if len(ret) == 0:
                    continue
                else:
                    self.recv_buf = self.recv_buf[spos:]
                    return ret
            try:
                num = int(line)
            except Exception as e:
                str(e)
                return []
            epos = (spos + num)

            if epos > len(self.recv_buf):
                break
            data = self.recv_buf[spos: epos]
            ret.append(data)
            spos = epos
            epos = self.recv_buf.find('\n', spos)

            if epos == -1:
                break
            epos += 1
        return None
