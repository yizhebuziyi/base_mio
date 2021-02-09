# -*- coding: utf-8 -*-
import os
import logging
import daiquiri
import daiquiri.formatter
from typing import Optional


class LogHandler(object):
    logger: daiquiri.KeywordArgumentAdapter

    def __init__(self, logger_name: str,
                 fmt: Optional[str] = '%(asctime)s [PID %(process)d] [%(levelname)s] %(name)s -> %(message)s',
                 datefmt: Optional[str] = None, logger_dir: Optional[str] = None, log_level: int = logging.DEBUG):
        formatter: daiquiri.formatter.ColorFormatter = daiquiri.formatter.ColorFormatter(
            fmt=fmt,
            datefmt=datefmt
        )
        if logger_dir:
            logger_path = os.path.join(logger_dir, logger_name)
            if not os.path.isdir(logger_path):
                os.makedirs(logger_path)
            daiquiri.setup(level=log_level, outputs=(
                daiquiri.output.Stream(formatter=formatter),
                daiquiri.output.File(logger_path, formatter=formatter),
            ))
        else:
            daiquiri.setup(level=log_level, outputs=(
                daiquiri.output.Stream(formatter=formatter),
            ))
        self.logger = daiquiri.getLogger(logger_name)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)
