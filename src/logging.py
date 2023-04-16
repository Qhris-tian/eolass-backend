import logging


LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"

logging.basicConfig(format=LOG_FORMAT_DEBUG)
