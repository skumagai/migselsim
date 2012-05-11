# -*- mode: python; coding: utf-8; -*-

from sys import stdout, stderr
import traceback

"""Handle logging messages"""

# inspired by @utahta's pythonbrew.log

class Color(object):
    END = '\033[0m'
    DEBUG = '\033[35mDEBUG' + END
    INFO = '\033[32mINFO' + END
    LOG = '\033[0mLOG' + END
    WARN = '\033[33mWARN' + END
    ERROR = '\033[31mERROR' + END

    @classmethod
    def _deco(cls, msg, color):
        return '{}: {}\n'.format(color, msg)

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
            to.write(Color.debug(msg))
        except Exception as e:
            self.error(e, stderr)

    def log(self, msg, to = stdout):
        try:
            to.write(Color.log(msg))
        except Exception as e:
            self.error(e, stderr)

    def info(self, msg, to = stdout):
        try:
            to.write(Color.info(msg))
        except Exception as e:
            self.error(e, stderr)

    def warn(self, msg, to = stderr):
        try:
            to.write(Color.warn(msg))
        except Exception as e:
            self.error(e, stderr)

    def error(self, msg, to = stderr):
        try:
            to.write(traceback.format_exc())
            to.write(Color.error(msg))
        except Exception as e:
            self.error(e, stderr)

logger = Logger()
