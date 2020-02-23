# @Author            : Dario Gonzalez
# @Date              : 2020-02-23
# @Last Modified by  : Dario Gonzalez
# @Last Modified time: 2020-02-23

import sys
from logging import Formatter, LoggerAdapter, getLogger, handlers

from properties.properties import (LOG_FORMATTER, LOG_LVL, LOG_NAME, LOG_PATH,
                                   LOG_ROTATE_INTERVAL, LOG_ROTATE_WHEN,
                                   LOG_TERMIN)

formatter = Formatter(LOG_FORMATTER, datefmt="%Y-%m-%d %H:%M:%S")

hdlrrot_file = handlers.TimedRotatingFileHandler(
    LOG_PATH + LOG_NAME + LOG_TERMIN,
    when=LOG_ROTATE_WHEN,
    interval=LOG_ROTATE_INTERVAL)

hdlrrot_file.setFormatter(formatter)
hdlrrot_file.setLevel(LOG_LVL)

logger = getLogger(LOG_NAME)
logger.setLevel(LOG_LVL)
logger.addHandler(hdlrrot_file)
