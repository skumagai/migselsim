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


class ConfigPlugin(Plugin):
    """
    Base class for config plugins.

    Plugins implementing this interface should provide the following attributes:

    :key:   The name of configuration key.

    :configure:  Code to handle config stanza.

    :requirment: Either "required" or "optional".

    :parent: Name of parental config snippet.  For top-level configs, use None.

    :conflict: Name of other config snippets, which specify the same aspect of simulations.
               Only one of those can be specified.

    :simple_entries: Names of config keys, which are not delegated to child plugins.
    """
    __metaclass__ = ConfigPluginMount

    @classmethod
    def action(cls, key):
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
