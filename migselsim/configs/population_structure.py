# -*- mode: python; coding: utf-8; -*-

from migselsim.configs import ConfigPlugin

class PopulationStructure(ConfigPlugin):
    key = 'population structure'
    requirement = 'required'
    parent = None
    conflict = None
    simple_entries = ()

    def configure(self, value, parent, simulator):
        PopulationStructure.verifyParent(parent)
        for item in value.iteritems():
            [key, val] = item
            if key in PopulationStructure.simple_entries:
                self.__getattr__(key)
            else:
                ConfigPlugin.action(key).configure(val,
                                              PopulationStructure.key,
                                              simulator)
