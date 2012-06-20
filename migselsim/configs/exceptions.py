# -*- mode: python; coding: utf-8; -*-

"""Exceptions used in config file parser."""

class ConfigException(Exception):
    """Base class for exception in this submodule."""
    pass

class ConflictingConfigOptionsError(ConfigException):
    """Exception raised if two contradicting configuration options are given.

    Attributes:
    :keys: contradicting keys
    :msg: explanation of error
    """

    def __init__(self, key, conflicts):
        self.key = key
        self.conflicts = conflicts

    def __str__(self):
        return 'conflicting configuration options: `{}`, `{}`'.format(self.key, self.conflicts)

class InvalidConfigValueError(ConfigException):
    """Exception raised for if a value is not valid for a configuration option.

    Attributes:
    :key: key
    :value: value
    :msg: explanation of error.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return 'invalid value for a node: (key: `{}`, value: `{}`)'.format(
            self.key, self.value)

class WrongConfigParentError(ConfigException):
    """Exception raised for a misplaced configuration option.

    Attributes:
    :key: key of current config plugin
    :parent: key of parent config plugin
    """

    def __init__(self, key, parent):
        self.key = key
        self.parent = parent

    def __str__(self):
        return 'wrong parent of `{}` node (parent: `{}`)'.format(
            self.key, self.parent)


class DuplicateConfigNodeError(ConfigException):
    """Exception raised if more than one config node have the same ID and if they are indistinguisable.

    Attributes:
    :key: key of current config plugin
    """

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return 'more than one node with id `{}`'.format(self.key)
