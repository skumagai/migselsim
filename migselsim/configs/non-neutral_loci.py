# -*- mode: python; coding: utf-8; -*-

import sys

from migselsim.configs import ConfigPlugin
from migselsim.definition import MALE, FEMALE, ALL_AVAIL
from migselsim.exception import LengthMismatchError
from migselsim.log import logger

class NonNeutralLoci(ConfigPlugin):
    key = 'non-neutral loci'
    requirement = 'optional'
    parent = 'chromosomes'
    conflict = None
    simple_entries = ()

    def configure(self, value, parent, simulator):
        self.verifyParent(parent)
        chrm_id = value[0]
        try:
            non_neutral_loci = simulator.non_neutral_loci
        except:
            non_neutral_loci = []

        for locus in value[1]:
            non_neutral_loci.append(_process_locus_data(chrm_id, locus))

        simulator.non_neutral_loci = non_neutral_loci

def _process_locus_data(chrom, locus):
    typeid = _get_type_of_locus(locus)
    if typeid == 1:
        # 1st type: sex- and deme-nonspecific
        return _sex_nonspecific_deme_nonspecific(chrom, locus)
    elif typeid == 2:
        # 2nd type: sex-nonspedific but deme-specific
        return _sex_nonspecific_deme_specific(chrom, locus)
    elif typeid == 3:
        # 3rd type: sex-specific but deme-nonspecific
        return _sex_specific_deme_nonspecific(chrom, locus)
    elif typeid == 4:
        # 4th type: sex- and deme-specific
        return _sex_specific_deme_specific(chrom, locus)

def _get_type_of_locus(locus):
    freq = locus['initial frequency']
    if type(freq) is dict:
        return 3
    elif type(freq[0]) is float:
        return 1
    elif type(freq[0]) is list:
        if type(freq[0][0]) is float:
            return 2
        else:
            return 4

def _check_consistency(nallele, freq, coeff):
    try:
        if nallele != len(freq):
            raise LengthMismatchError('initial frequency', nallele, len(freq))
        coeff_exp = nallele + (nallele * (nallele - 1)) / 2
        if coeff_exp != len(coeff):
            raise LengthMismatchError('selection coefficient', coeff_exp, len(coeff))

        for homoez in ((i,i) for i in range(nallele)):
            if homoz not in coeff:
                raise MissingGenotypeError(homez)
        for heteroz in ((i,j) for i in range(nallele) for j in range(i+1,nallele)):
            if heteroz not in coeff:
                raise MissingGenotypeError(heteroz)
    except Exception e:
        logger.error(e)
        sys.exit(1)


# typ1
def _sex_nonspecific_deme_nonspecific(chrom, locus):
    _check_consistency(locus['number of alleles'],
                       locus['initial frequency'],
                       locus['selection coefficient'])

    return [{prop: locus['initial frequency'],
             coeff: locus['selection coefficient'],
             chromosome: chrom,
             position: locus['position'],
             deme: ALL_AVAIL,
             sex: ALL_AVAIL}]


# type2
def _sex_nonspecific_deme_specific(chrom, locus):
    data = []
    nallele = locus['number of alleles']
    pos = locus['position']
    for idx, vals in enumerate(zip(locus['initial frequency'],
                                   locus['selection coefficient'])):
        [freq, coeff] = vals
        _check_consistency(nallele, freq, coeff)
        data.append({prop: freq,
                     coeff: coeff,
                     chromosome: chrom,
                     position: pos,
                     deme: idx,
                     sex: ALL_AVAIL})
    return data

def _sex_specific_deme_nonspecific(chrom, locus):
    data = []
    sexes = ['male', 'female']
    nallele = locus['number of alleles']
    pos = locus['position']
    freq = locus['initial frequency']
    coeff = locus['selection coefficient']
    pos = locus['position']
    for sex in sexes:
        if sex == 'male':
            s = MALE
        else:
            s = FEMALE
        _check_consistency(nallele, freq[sex], coeff[sex])
        data.append({prop: locus['initial frequency'][sex],
                     coeff: locus['selection coefficient'][sex],
                     chromosome: chrom,
                     position: pos,
                     deme: ALL_AVAIL,
                     sex: s})
    return data

def _sex_specific_deme_specific(chrom, locus):
    data = []
    sexes = ['male', 'female']
    nallele = locus['number of alleles']
    pos = locus['position']
    for idx, vals in enumerate(zip(locus['initial frequency'],
                                   locus['selection coefficient'])):
        freq, coeff = vals
        for sex in sexes:
            if sex == 'male':
                s = MALE
            else:
                s = FEMALE
            _check_consistency(nallele, freq[sex], coeff[sex])
            data.append({prop: freq[sex],
                         coeff: coeff[sex],
                         chromosome: chrom,
                         position: pos,
                         deme: idx,
                         sex: s})
    return data