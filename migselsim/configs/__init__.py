# -*- mode: python; coding: utf-8; -*-

import os
import sys

import yaml

from migselsim.baseplugin import PluginMount, Plugin
from migselsim.simulator import Simulator
from migselsim.exception import WrongConfigParentError

# Register config plugins by scanning the directory and import all modules.
# Imported plugins are normal python file (*.py), and their names need not
# start with '__' such as (__init__.py).

class ConfigPluginMount(PluginMount):
    """
    Parental class of all config plugins.

    All plugins inherited from this class are registered in ConfigPluginMount dict.
    """
    pass


class ConfigRecipe(Plugin):
    """
    Configure simulator given a node of configuration tree.

    Any class implementing this interface should provide the following attributes:

    :key: Name of configuration key.

    :child: List of names of child nodes.  Terminal nodes take None for this variable.  Used for validation.

    :parent: Name of parental node.  Root node takes None for this variable.  Used for validation.

    :conflict: List of names of conflicting config nodes.  Two nodes are in conflict when
    two nodes specify the same aspect of simulations.

    """
    __metaclass__ = ConfigPluginMount

    instances = {}

    @classmethod
    def action(cls, key):
        # return cached instance of invoked class if the class is already
        # instantiated.  Otherwise instantiate the class and return the
        # new instance.
        if not key in cls.instances:
            cls.instances[key] = cls.plugins[key]()
        return ConfigPlugin.plugins[key]()

    @classmethod
    def verifyParent(cls, parent):
        try:
            parent = parent.lower()
        except:
            pass
        if parent != cls.parent:
            raise WrongConfigParentError(cls.key, parent)

    def configure(self, value, parent, simulator):
        raise NotImplementedError

def parse_config(stream):
    """Parse a YAML-formated configuration file, and apply appropriate settings."""
    data = yaml.load_all(stream)
    simulators = []
    ConfigPlugin.scan()
    for datum in data:
        sim = Simulator()
        for item in datum.iteritems():
            key, value = item
            ConfigPlugin.action(key).configure(value, None, sim)

        simulators.append(sim)
    return simulators
