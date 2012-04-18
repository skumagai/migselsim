# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class NumberOfReplicates(ConfigPlugin):
    key = 'number of replicates'
    requirment = 'required'
    parent = None
    conflict = None

    def main(self, value, parent):
        pass
