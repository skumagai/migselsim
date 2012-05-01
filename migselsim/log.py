# -*- mode: python; coding: utf-8; -*-

from sys import stdout, stderr

"""Handle logging messages"""

# inspired by @utahta's pythonbrew.log

class Color(object):
    DEBUG = '\033[35m'
    INFO = '\033[32m'
    LOG = '\033[0m'
    WARN = '\033[33m'
    ERROR = '\033[31m'
    END = '\033[0m'

    @classmethod
    def _deco(cls, msg, color):
        return '{}{}{}'.format(color, msg, cls.END)

    @classmethod
    def debug(cls, msg):
        return cls._deco(msg, cls.DEBUG)

    @classmethod
    def info(cls, msg):
        return cls._deco(msg, cls.INFO)

    @classmethod
    def log(cls, msg):
        return cls._deco(msg, cls.LOG)

    @classmethod
    def warn(cls, msg):
        return cls._deco(msg, cls.WARN)

    @classmethod
    def error(cls, msg):
        return cls._deco(msg, cls.ERROR)

class Logger(object):

    def debug(self, msg, to = stderr):
        try:
            to.write(Color.debug('DEBUG: {}\n'.format(msg)))
        except Exception as e:
            self.error(e, stderr)

    def log(self, msg, to = stdout):
        try:
            to.write(Color.log('{}\n'.format(msg)))
        except Exception as e:
            self.error(e, stderr)

    def info(self, msg, to = stdout):
        try:
            to.write(Color.info('INFO: {}\n'.format(msg)))
        except Exception as e:
            self.error(e, stderr)

    def warn(self, msg, to = stderr):
        try:
            to.write(Color.warn('WARN: {}\n'.format(msg)))
        except Exception as e:
            self.error(e, stderr)

    def error(self, msg, to = stderr):
        try:
            to.write(Color.error('ERROR: {}\n'.format(msg)))
        except Exception as e:
            self.error(e, stderr)

logger = Logger()
