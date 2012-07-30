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
from simuPOP import MALE, FEMALE, UNIFORM_DISTRIBUTION, \
    AUTOSOME, CHROMOSOME_X, CHROMOSOME_Y, MITOCHONDRIAL, ALL_AVAIL, \
    PER_LOCI, PER_INDIVIDUAL, PER_PLOIDY, PER_CHROMOSOME, \
    BY_PROBABILITY, BY_PROPORTION, PROB_OF_MALES

# metadata of this package.  This is likely to change once I start
# to use distutils2/packaging instead of setuptools/distutils.
# Then metadata is defined in PKG-INFO file.
from migselsim import metadata

def enum(*seq, **named):
    enums = dict(zip(seq, range(len(seq))), **named)
    return type('Enum', (), enums)

SCENARIO = enum('NOT_SPECIFIC', 'SEX_SPECIFIC', 'DEME_SPECIFIC', 'SEX_AND_DEME_SPECIFIC')

COMMAND = __name__.split('.')[0]
VERSION = metadata.__version__

# indicating that a parameter does not show population- or
# sex-specificity.
NO_STRUCTURE = -10
