# -*- mode: python; coding: utf-8; -*-

from melsigsem.baseconfig import PluginMount

class ConfigPluginMount(PluginMount):
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
