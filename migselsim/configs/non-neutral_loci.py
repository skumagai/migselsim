# -*- mode: python; coding: utf-8; -*-

import sys

from migselsim.configs import ConfigRecipe
from migselsim.definition import MALE, FEMALE, ALL_AVAIL, NO_STRUCTURE
from migselsim.exception import LengthMismatchError
from migselsim.log import logger

class NonNeutralLoci(ConfigRecipe):
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
            non_neutral_loci.extend(_process_locus_data(chrm_id, locus))

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

def _convert_tuple(coeff):
    """Convert keys of dict e.g. '(1,2)' (string) to (1,2) (tuple of integer)."""
    new_dict = {}
    for key, value in coeff.iteritems():
        new_dict[tuple(int(i) for i in key[1:-1].split(','))] = value
    return new_dict

def _check_consistency(nallele, freq, coeff):
    try:
        if nallele != len(freq):
            raise LengthMismatchError('initial frequency', nallele, len(freq))
        coeff_exp = nallele + (nallele * (nallele - 1)) / 2
        if coeff_exp != len(coeff):
            raise LengthMismatchError('selection coefficient', coeff_exp, len(coeff))

        for homoz in ((i,i) for i in range(nallele)):
            if homoz not in coeff:
                raise MissingGenotypeError(homez)
        for heteroz in ((i,j) for i in range(nallele) for j in range(i+1,nallele)):
            if heteroz not in coeff:
                raise MissingGenotypeError(heteroz)
    except Exception as e:
        logger.error(e)
        sys.exit(1)


# type1
def _sex_nonspecific_deme_nonspecific(chrom, locus):
    coeff = _convert_tuple(locus['selection coefficient'])
    _check_consistency(locus['number of alleles'],
                       locus['initial frequency'],
                       coeff)

    return [_construct_entry(locus['initial frequency'], coeff, chrom, locus['position'],
                             NO_STRUCTURE, NO_STRUCTURE)]


# type2
def _sex_nonspecific_deme_specific(chrom, locus):
    data = []
    nallele = locus['number of alleles']
    pos = locus['position']
    for idx, vals in enumerate(zip(locus['initial frequency'],
                                   locus['selection coefficient'])):
        [freq, coeff] = vals
        coeff = _convert_tuple(coeff)
        _check_consistency(nallele, freq, coeff)
        data.append(_construct_entry(freq, coeff, chrom, pos, idx, NO_STRUCTURE))
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
        c = _convert_tuple(coeff[sex])
        _check_consistency(nallele, freq[sex], c)
        data.append(_convert_tuple(locus['initial frequency'][sex],
                                   locus['selection coefficient'][sex],
                                   chrom, pos, NO_STRUCTURE, s))
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
            c = _convert_tuple(coeff[sex])
            _check_consistency(nallele, freq[sex], c)
            data.append(_construct_entry(freq[sex], coeff[sex], chrom, pos, idx, s))
    return data

def _construct_entry(freq, coeff, chrom, pos, deme, sex):
    return {'prop': freq,
            'coeff': coeff,
            'chromosome': chrom,
            'position': pos,
            'deme': deme,
            'sex': sex}
