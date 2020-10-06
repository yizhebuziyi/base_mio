# -*- coding: utf-8 -*-
import os
import logging
import logging.handlers


class LogHandler(object):
    logger = None

    def __init__(self, logger_name, fmt=None, log_file=None, log_level=logging.DEBUG):
        if logger_name is None or not isinstance(logger_name, str):
            print(u'logger_name must be str.')
            exit()
        fmt = '%(asctime)s - %(name)s - %(message)s' if fmt is None else fmt.strip()
        formatter = logging.Formatter(fmt)  # 实例化formatter
        file_handler = None
        log_file = '' if log_file is None else log_file.strip()
        if len(log_file) > 0:
            # 判断是否存在文件夹
            dirs = os.path.split(log_file)
            if len(dirs) > 1:
                path = dirs[0]
                if not os.path.exists(path):
                    try:
                        os.makedirs(path)
                    except Exception as e:
                        print(u'Can\'t create folder：')
                        print(e)
                        exit()
            file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024 * 1024,
                                                                backupCount=5, encoding='utf-8')
            file_handler.setFormatter(formatter)  # 为handler添加formatter
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(console_handler)
        if file_handler is not None:
            self.logger.addHandler(file_handler)
        if log_level is None or not isinstance(log_level, int):
            log_level = logging.DEBUG
        else:
            log_level = int(log_level)
        self.logger.setLevel(log_level)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def close(self):
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)
