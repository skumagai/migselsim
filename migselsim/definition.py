# -*- mode: python; coding: utf-8; -*-

"""Import simuPOP's function and constant names."""

# import functions
import simuOpt
# we unconditionally use 'lineage' version of simuPOP as our interest is lineage.
simuOpt.setOptions(quiet = True,
                   alleleType = 'lineage')
from simuPOP import RandomMating, getRNG
import simuPOP

# import constants
from simuPOP import MALE, FEMALE, UNIFORM_DISTRIBUTION, HAPLODIPLOID, \
    AUTOSOME, CHROMOSOME_X, CHROMOSOME_Y, MITOCHONDRIAL

# metadata of this package.  This is likely to change once I start
# to use distutils2/packaging instead of setuptools/distutils.
# Then metadata is defined in PKG-INFO file.
from migselsim import metadata

COMMAND = __name__.split('.')[0]
VERSION = metadata.__version__
