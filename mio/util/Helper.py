# -*- coding: utf-8 -*-
import os
import re
import zlib
import base64
import random
import string
import hashlib
import time
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from flask import request
from typing import Any, Tuple, Union, Optional, List, Dict
from daiquiri import KeywordArgumentAdapter


def in_dict(dic: dict, key: str) -> bool:
    for kt in dic.keys():
        if kt == key:
            return True
    return False


def is_enable(dic: dict, key: str) -> bool:
    if not in_dict(dic, key):
        return False
    _ = dic[key]
    if not isinstance(_, bool):
        return False
    return _


def get_real_ip() -> str:
    real_ip: str = ''
    if 'HTTP_CF_CONNECTING_IP' in request.environ:
        real_ip = request.environ['HTTP_CF_CONNECTING_IP']
    elif 'HTTP_X_CLIENT' in request.environ:
        real_ip = request.environ['HTTP_X_CLIENT']
    elif 'HTTP_FORWARDED' in request.environ:
        http_forwarded: str = str(request.environ['HTTP_FORWARDED'])
        xp = http_forwarded.split(';')
        for s in xp:
            if s.startswith('for='):
                _, real_ip, *_ = s.split('=')
                break
    if len(real_ip) > 0:
        return real_ip
    if 'HTTP_X_REAL_IP' in request.environ:
        real_ip = request.environ['HTTP_X_REAL_IP']
    elif 'HTTP_X_FORWARDED_FOR' in request.environ:
        real_ip = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        real_ip = request.environ['REMOTE_ADDR']
    return real_ip


def timestamp2str(timestamp: int, iso_format: str = '%Y-%m-%d %H:%M:%S', tz: int = 8,
                  logger: Optional[KeywordArgumentAdapter] = None) -> Optional[str]:
    dt = None
    try:
        utc_time = datetime.fromtimestamp(timestamp)
        local_dt = utc_time + timedelta(hours=tz)
        dt = local_dt.strftime(iso_format)
    except Exception as e:
        if logger:
            logger.error(e)
    return dt


def str2timestamp(date: str, iso_format: str = '%Y-%m-%d %H:%M:%S',
                  logger: Optional[KeywordArgumentAdapter] = None) -> Optional[int]:
    ts = None
    try:
        time_array = time.strptime(date, iso_format)
        timestamp = time.mktime(time_array)
        ts = int(timestamp)
    except Exception as e:
        if logger:
            logger.error(e)
    return ts


def get_bool(obj) -> bool:
    obj = False if obj is None else obj
    if isinstance(obj, bool) is False:
        if is_number(obj):
            obj = True if int(obj) == 1 else False
        elif isinstance(obj, str):
            obj = True if obj.lower() == "y" or obj.lower() == "t" else False
        else:
            obj = False
    return obj


def get_int(obj: Any) -> int:
    obj = 0 if is_number(obj) is False else int(obj)
    return obj


def get_root_path() -> str:
    root_path = os.path.abspath(os.path.dirname(__file__) + '/../../')
    return root_path


def file_lock(filename: str, txt: str = ' ', exp: int = None, reader: bool = False) -> Tuple[int, str]:
    lock = os.path.join(get_root_path(), 'lock')
    if not os.path.exists(lock):
        os.makedirs(lock)
    lock = os.path.join(lock, filename)
    if not os.path.isfile(lock):
        is_ok, txt = write_txt_file(lock, txt)
        return -1 if not is_ok else 1, txt
    # 如果文件存在，则判断是否需要检测过期
    if exp is None or not is_number(exp):
        return 0, u'Locked.' if not reader else read_txt_file(lock)
    exp = int(exp)
    if exp <= 0:
        return 0, u'Locked.' if not reader else read_txt_file(lock)
    exp = int(exp * 60)  # 是否有超过界限的问题？
    file_time = int(os.stat(lock).st_mtime)
    if exp >= (int(time.time()) - file_time):
        os.unlink(lock)
        return file_lock(filename, txt, exp)
    # 判断是否要读取内容
    return 0, u'Locked.' if not reader else read_txt_file(lock)


def write_txt_file(filename: str, txt: str = ' ', encoding: str = 'utf-8') -> Tuple[bool, str]:
    if os.path.isfile(filename):
        os.unlink(filename)
    try:
        with open(filename, 'w', encoding=encoding) as locker:
            locker.write(txt)
        return True, txt
    except Exception as e:
        return False, str(e)


def read_txt_file(filename: str, encoding: str = 'utf-8') -> str:
    if not os.path.isfile(filename):
        return ''
    with open(filename, 'r', encoding=encoding) as reader:
        txt = reader.read()
    return txt


def write_file(filename: str, txt: Union[str, bytes] = ' ', method: str = 'w+', encoding: str = 'utf-8') \
        -> Tuple[bool, str]:
    try:
        with open(filename, method, encoding=encoding) as locker:
            locker.write(txt)
        return True, txt
    except Exception as e:
        return False, str(e)


def read_file(filename: str, method: str = 'r', encoding: str = 'utf-8') -> Optional[Union[str, bytes]]:
    if not os.path.isfile(filename):
        return None
    with open(filename, method, encoding=encoding) as reader:
        txt = reader.read()
    return txt


def file_unlock(filename: str) -> Tuple[int, str]:
    lock: str = os.path.join(get_root_path(), 'lock')
    if not os.path.exists(lock):
        return 1, u'Unlocked.'
    try:
        lock = os.path.join(lock, filename)
        if os.path.isfile(lock):
            os.unlink(lock)
        return 1, u'Locked.'
    except Exception as e:
        return -1, str(e)


def random_str(random_length: int = 8) -> str:
    a: List[str] = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:random_length])


def random_number_str(random_length: int = 8) -> str:
    a: List[str] = [str(0), str(1), str(2), str(3), str(4), str(5), str(6), str(7), str(8), str(9)]
    random.shuffle(a)
    return ''.join(a[:random_length])


def random_char(size: int = 6, special: bool = False) -> str:
    import random
    import string
    chars = string.ascii_letters + string.digits
    if special:
        chars += '!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(size))


def get_file_list(root_path: Optional[str] = None, files: Optional[List[str]] = None, is_sub: bool = False,
                  is_full_path: bool = True, include_hide_file: bool = False) -> List[str]:
    if root_path is None or files is None or not isinstance(files, list):
        return files if isinstance(files, list) else []
    for lists in os.listdir(root_path):
        if lists.startswith('.') or lists.endswith('.pyc'):
            if not include_hide_file:
                continue
        if is_full_path:
            path = os.path.join(root_path, lists)
        else:
            path = lists
        if is_sub and os.path.isdir(os.path.join(root_path, lists)):
            files = get_file_list(root_path=os.path.join(root_path, lists), files=files, is_sub=is_sub,
                                  is_full_path=is_full_path)
        else:
            files.append(path)
    return files


def check_file_in_list(file: Optional[str] = None, file_list: List[str] = None) -> bool:
    if file is None or not isinstance(file, str) or \
            file_list is None or not isinstance(file_list, list):
        return False
    file = file.lower()
    if file in file_list:
        return True
    for f in file_list:
        if file.startswith(f.lower()):
            return True
    return False


def crc_file(file_name: str) -> str:
    prev = 0
    for eachLine in open(file_name, "rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X" % (prev & 0xFFFFFFFF)


def is_number(s: Any) -> bool:
    if s is not None:
        try:
            s = str(s)
        except ValueError:
            return False
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

    return False


def self_html_code(string_html: str = '', is_all: bool = True) -> str:
    # 如果is_all为True，则过滤掉全部的<>
    if string_html is None:
        return ''
    string_html = string_html if isinstance(string_html, str) else str(string_html)
    if is_all:
        return string_html.replace('<', '&lt;').replace('>', '&gt;').replace('%3C', '&lt;').replace('%3E', '&gt;')
    # 保留安全的，默认只处理script、object和iframe
    # 直接用转意符写的肯定有问题，直接处理掉
    string_html = string_html.replace('%3C', '&lt;').replace('%3E', '&gt;')
    re_script_start = re.compile('<\s*script[^>]*>', re.IGNORECASE)  # Script 开始
    re_script_end = re.compile('<\s*/\s*script\s*>', re.IGNORECASE)  # Script 结束
    re_object_start = re.compile('<\s*object[^>]*>', re.IGNORECASE)  # object 开始
    re_object_end = re.compile('<\s*/\s*object\s*>', re.IGNORECASE)  # object 结束
    re_iframe_start = re.compile('<\s*iframe[^>]*>', re.IGNORECASE)  # iframe 开始
    re_iframe_end = re.compile('<\s*/\s*iframe\s*>', re.IGNORECASE)  # iframe 结束
    string_html = re_script_start.sub('', string_html)  # 直接去掉
    string_html = re_script_end.sub('', string_html)
    string_html = re_object_start.sub('', string_html)
    string_html = re_object_end.sub('', string_html)
    string_html = re_iframe_start.sub('', string_html)
    string_html = re_iframe_end.sub('', string_html)
    return string_html


def ant_path_matcher(ant_path: str, expected_path: str) -> bool:
    star = r"[^\/]+"
    double_star = r".*"
    slash = r"\/"
    question_mark = r"\w"
    dot = r"\."

    output = ant_path.replace(r"/", slash).replace(r".", dot)
    output = re.sub(r"(?<!\*)\*(?!\*)", star, output)
    output = output.replace(r"**", double_star)
    output = output.replace(r"?", question_mark)
    rc = re.compile(output, re.IGNORECASE)
    if rc.match(expected_path) is None:
        return False
    return True


def check_email(email: str) -> bool:
    re_str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    if re.match(re_str, email) is None:
        return False
    return True


def get_args_from_dict(dt: Dict, ky: str, default: Optional[Any] = '') -> Optional[Any]:
    word = default if ky not in dt else dt[ky]
    if is_number(word):
        return word
    if isinstance(word, str):
        return str(word).strip()
    return word


def get_variable_from_request(key_name: str, default: Optional[str] = '', method: str = 'check') -> Optional[Any]:
    method = 'check' if method is None or not isinstance(method, str) else str(method).strip().lower()
    if method == 'check':
        word = request.form.get(key_name, None)
        if word is None:
            word = request.args.get(key_name, None)
            if key_name in request.headers:
                word = request.headers[key_name]
        word = default if word is None else word
    elif method == 'post':
        word = request.form.get(key_name, default)
    elif method == 'get':
        word = request.args.get(key_name, default)
    elif method == 'header':
        word = request.headers[key_name] if key_name in request.headers else default
    else:
        return default
    if word is None:
        return default
    if is_number(word):
        return word
    return str(word).strip()


def get_utc_now() -> int:
    dt = int(time.mktime(datetime.now(timezone.utc).timetuple()))
    return dt


def microtime(get_as_float=False, max_ms_lan: int = 6) -> str:
    d = datetime.now()
    t = time.mktime(d.timetuple())
    ms: float = d.microsecond / 1000000.
    if get_as_float:
        ms_txt = str(ms)
        if len(ms_txt) >= max_ms_lan + 2:
            ms_txt = ms_txt[:max_ms_lan + 2]
        else:
            max_loop: int = (max_ms_lan - len(ms_txt)) + 2
            for i in range(max_loop):
                ms_txt = '{}0'.format(ms_txt)
        txt_long = '0.'
        for i in range(max_ms_lan):
            txt_long = '{}0'.format(txt_long)
        a = Decimal(ms_txt).quantize(Decimal(txt_long))
        b = Decimal(t)
        dt = a + b
        return str(dt)
    else:
        return '%f %d' % (ms, t)


def md5(txt: str) -> str:
    md = hashlib.md5()
    md.update(txt.encode('utf-8'))
    return md.hexdigest()


def base64_encode(message: bytes, is_bytes: bool = False) -> Union[bytes, str]:
    crypto: bytes = base64.b64encode(message)
    if is_bytes:
        return crypto
    return crypto.decode('utf-8')


def base64_decode(crypto: str, is_bytes: bool = False) -> Union[bytes, str]:
    message: bytes = base64.b64decode(crypto)
    if is_bytes:
        return message
    return message.decode('utf-8')


def base64_txt_encode(message: str) -> str:
    return str(base64_encode(message.encode('utf-8')))


def base64_txt_decode(crypto: str) -> str:
    return str(base64_decode(crypto))
