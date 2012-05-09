# -*- mode: python; coding: utf-8; -*-

"""Exceptions used in config file parser."""

class ConfigException(Exception):
    """Base class for exception in this submodule."""
    pass

class KeyConflictError(ConfigException):
    """Exception raised for error if two contradicting keys are specified.

    Attributes:
    :keys: contradicting keys
    :msg: explanation of error
    """

    def __init__(self, keys):
        self.keys = keys

    def __str__(self):
        return 'keys cotradicted: `{}`, `{}`'.format(*self.keys)

class InvalidConfigValueError(ConfigException):
    """Exception raised for error if a value is not valid for a key.

    Attributes:
    :key: key
    :value: value
    :msg: explanation of error.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return 'invalid value for a key: (key: `{}`, value: `{}`)'.format(
            self.key, self.value)

class WrongConfigParentError(ConfigException):
    """Exception raised for error if a config key is invoked in a wrong context.

    Attributes:
    :key: key of current config plugin
    :parent: key of parent config plugin
    """

    def __init__(self, key, parent):
        self.key = key
        self.parent = parent

    def __str__(self):
        return 'config `{}` is invoked from a wrong parent `{}`'.format(
            self.key, self.parent)


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
