# -*- mode: python; coding: utf-8; -*-

import os
import sys

import yaml

from migselsim.baseplugin import PluginMount
from migselsim.core import Simulator

# Register config plugins by scanning the directory and import all modules.
# Imported plugins are normal python file (*.py), and their names need not
# start with '__' such as (__init__.py).

class ConfigPluginMount(PluginMount):
    """
    Parental class of all config plugins.

    All plugins inherited from this class are registered in ConfigPluginMount dict.
    """
    pass


class ConfigPlugin(object):
    """
    Mount point for plugins which refer to actions that can be performed.

    Plugins implementing this reference should provide the following attributes:

    :key:   The name of configuration key.

    :main:  Entry point to an action associating with the configuration key.

    :requirment: Importance of the key. Either "required" or "optional".  If left undefined, the key is treated optional.

    :parent: A name of parental key for a nested key.  If left undefined, the key is treated as a top-level key.

    :conflict: Other configuration keys that conflict with the action specified by this key.  If left undefined, there is no conflict.
    """
    __metaclass__ = ConfigPluginMount

    @classmethod
    def action(cls, key):
        return ConfigPlugin.plugins[key]()

    @classmethod
    def verifyParent(cls, parent):
        try:
            parent = parent.lower
        except:
            pass
        if parent != cls.parent:
            raise ValueError

    def main(self, value, parent, simulator):
        raise NotImplementedError

def import_plugins():
    path = os.path.abspath(os.path.dirname(__file__))
    for module in [m[:-3]  for m in os.listdir(path)
                   if m[-3:] == '.py' and m[:2] != '__' and m[0] != '.']:

        # construct absolute pass of a module to be imported.
        module = __name__ + '.' + module
        if not module in sys.modules:
            # skip if the module has been already imported.
            try:
                __import__(module)
            except ImportError:
                # silently ignore failed import
                pass

def parse_config(stream):
    """Parse a YAML-formated configuration file, and apply appropriate settings."""
    data = yaml.load_all(stream)
    for datum in data:
        sim = Simulator()
        for item in datum.iteritems():
            key, value = item
            ConfigPlugin.action(key).main(value, None, sim)
        print sim.__dict__

import_plugins()
