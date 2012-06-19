# -*- mode: python; coding: utf-8; -*-

"""Set genetic structure of simulated indiviudals.

Simple settings are handles are directly handled by this, but more complex
settings are delegated to specialized plugins.
"""

from migselsim.configs import ConfigRecipe

class GeneticStructure(ConfigRecipe):
    key = 'genetic structure'
    requirement = 'required'
    parent = None
    conflict = None


    def configure(self, value, parent, simulator):
        self.verifyParent(parent)

        for key in value:
            lkey = key.lower()
            lkey = lkey.replace(' ', '_')
            self.action(key).configure(value[key], self.key, simulator)
