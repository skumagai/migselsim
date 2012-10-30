# -*- mode: python; coding: utf-8; -*-

"""Exceptions used in config file parser."""

class ConfigException(Exception):
    """Base class for exception in this submodule."""
    pass

class ConflictingNodes(ConfigException):
    """Nodes conflict with each other."""
    pass

class WrongValue(ConfigException):
    """Value of a node is wrong."""
    pass

class MissingValue(ConfigException):
    """Value is missing."""
    pass

class WrongPosition(ConfigException):
    """Node is at a wrong location in a tree."""
    pass

class NodeRepeated(ConfigException):
    """A node is repeated more than allowed."""
    pass

class NodeNotFound(ConfigException):
    """Requested node is not found."""
    pass


class LengthesMismatched(ConfigException):
    """lengths of two or more lists/dict do not match."""
    pass
