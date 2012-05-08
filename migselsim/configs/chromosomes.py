# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin
from migselsim.definition import CHROMOSOME_X, CHROMOSOME_Y, AUTOSOME, MITOCHONDRIAL

_chromType = {'x': CHROMOSOME_X,
              'y': CHROMOSOME_Y,
              'autosome': AUTOSOME,
              'mitochondria': MITOCHONDRIAL}

class Chromosomes(ConfigPlugin):
    key = 'chromosomes'
    requirement = 'required'
    parent = 'genetic structure'
    conflict = None
    simple_entries = ('type', 'id', 'number of loci')

    def configure(self, value, parent, simulator):
        self.verifyParent(parent)
        simulator.chromTypes = []
        simulator.chromNames = []
        simulator.loci = []
        for idx, chrom in enumerate(value):
            for key, value in chrom.iteritems():
                if key in self.simple_entries:
                    lkey = key.replace(' ', '_').lower()
                    self.__getattribute__(lkey)(value, simulator)
                else:
                    self.action(key).configure([idx, value], self.key, simulator)

    def type(self, value, simulator):
        simulator.chromTypes.append(_chromType[value])

    def id(self, value, simulator):
        simulator.chromNames.append(value)

    def number_of_loci(self, value, simulator):
        simulator.loci.append(int(value))
