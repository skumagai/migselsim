# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin
from migselsim.definition import MALE, FEMALE, ALL_AVAIL

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
    try:
        if 'male' in freq:
            return 3
        else:
            try:
                'male' in freq[0]
                return 4
            except:
                return 2
    except:
        return 1

def _sex_nonspecific_deme_nonspecific(chrom, locus):
    return [{prop: [locus['initial frequency'], 1 - locus['initial frequency']],
             chromosome: chrom,
             position: locus['position'],
             deme: ALL_AVAIL,
             sex: ALL_AVAIL}]

def _sex_nonspecific_deme_specific(chrom, locus):
    data = []
    for idx, freq in enumerate(locus['initial frequency']):
        data.append({prop: [freq, 1 - freq],
                     chromosome: chrom,
                     position: locus['position'],
                     deme: idx,
                     sex: ALL_AVAIL})
    return data

def _sex_specific_deme_nonspecific(chrom, locus):
    data = []
    sexes = ['male', 'female']
    freq = locus['initial frequency']
    for sex in sexes:
        if sex == 'male':
            s = MALE
        else:
            s = FEMALE
        data.append({prop: [freq[sex], 1 - freq[sex]],
                     chromosome: chrom,
                     position: locus['position'],
                     deme: ALL_AVAIL,
                     sex: s})
    return data

def _sex_specific_deme_specific(chrom, locus):
    data = []
    sexes = ['male', 'female']
    freqs = locus['initial frequency']
    for idx, freq in enumerate(freqs):
        for sex in sexes:
            if sex == 'male':
                s = MALE
            else:
                s = FEMALE
            data.append({prop: [freq[sex], 1 - freq[sex]],
                         chromosome: chrom,
                         position: locus['position'],
                         deme: idx,
                         sex: s})
    return data
