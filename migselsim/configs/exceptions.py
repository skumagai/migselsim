# -*- mode: python; coding: utf-8; -*-

"""Exceptions used in config file parser."""

class ConfigException(Exception):
    """Base class for exception in this submodule."""
    pass

class KeyConflictError(ConfigException):
    """Exception raised if two contradicting configuration options are given.

    Attributes:
    :keys: contradicting keys
    :msg: explanation of error
    """

    def __init__(self, key1, key2):
        self.keys = (key1, key2)

    def __str__(self):
        return 'config options conflicted: {}'.format(self.keys)

class InvalidValueError(ConfigException):
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

class InvalidNodePositionError(ConfigException):
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


class DuplicateNodeError(ConfigException):
    """Exception raised if more than one config node have the same ID and if they are indistinguisable.

    Attributes:
    :key: key of current config plugin
    """

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return 'more than one node with id `{}`'.format(self.key)

class LengthMismatchError(ConfigException):
    """Exception raised when number of alleles does not match with number of initial frequencies

    Attributes:
    :entry: name of configuration entry
    :expected: expected length of sequence
    :observed: observed length of sequence
    """

    def __init__(self, entry, expected, observed):
        self.entry = entry
        self.expected = expected
        self.observed = observed

    def __str__(self):
        return 'length mismatch for {}: expected `{}`, obtained `{}`'.format(
            self.entry, self.expected, self.observed)

class MissingGenotypeError(ConfigException):
    """Exception raised when selection coefficient is not specified for a genotype.

    Attributes:
    :genotype: missing genotype
    """

    def __init__(self, genotype):
        self.genotype = genotype

    def __str__(self):
        return 'selection coefficient missing for a genotype: `{}`'.format(self.genotype)
