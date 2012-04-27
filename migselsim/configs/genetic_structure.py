# -*- mode: python; coding: utf-8; -*-

"""Set genetic structure of simulated indiviudals.

Simple settings are handles are directly handled by this, but more complex
settings are delegated to specialized plugins.
"""

from migselsim.configs import ConfigPlugin

class GeneticStructure(ConfigPlugin):
    key = 'genetic structure'
    requirement = 'required'
    parent = None
    conflict = None

    simple_keys = ('ploidy')

    def configure(self, value, parent, simulator):
        GeneticStructure.verifyParent(parent)
        # for datum in value:
        #     datum
