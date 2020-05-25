import logging
import os
from logging.handlers import TimedRotatingFileHandler
import qaconfig

BASIC_LOG_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


def log():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    _log_all_when = qaconfig.LogConstant.all_when
    _log_all_backupCount = qaconfig.LogConstant.all_backupCount

    _log_error_when = qaconfig.LogConstant.error_when
    _log_error_backupCount = qaconfig.LogConstant.error_backupCount

    # handler all
    handler = TimedRotatingFileHandler(BASIC_LOG_PATH + "/log/qa_all.log", when=_log_all_when, backupCount=_log_all_backupCount)
    datefmt = "%Y-%m-%d %H:%M:%S"
    format_str = "[%(asctime)s]: [%(filename)s] [%(levelname)s] [%(lineno)s] %(message)s"
    formatter = logging.Formatter(format_str, datefmt)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    # handler error
    handler = TimedRotatingFileHandler(BASIC_LOG_PATH + "/log/qa_error.log", when=_log_error_when, backupCount=_log_error_backupCount)
    datefmt = "%Y-%m-%d %H:%M:%S"
    format_str = "[%(asctime)s]: [%(filename)s] [%(levelname)s] [%(lineno)s] %(message)s"
    formatter = logging.Formatter(format_str, datefmt)
    handler.setFormatter(formatter)
    handler.setLevel(logging.ERROR)
    logger.addHandler(handler)

    return logger
