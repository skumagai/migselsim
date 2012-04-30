# -*- mode: python; coding: utf-8; -*-

"""Import simuPOP's function and constant names."""

# import functions
import simuOpt
simuOpt.setOptions(quiet = True)
from simuPOP import RandomMating

# import constants
from simuPOP import MALE, FEMALE, UNIFORM_DISTRIBUTION, getRNG

# metadata of this package.  This is likely to change once I start
# to use distutils2/packaging instead of setuptools/distutils.
# Then metadata is defined in PKG-INFO file.
from migselsim import metadata

COMMAND = __name__.split('.')[0]
VERSION = metadata.__version__
