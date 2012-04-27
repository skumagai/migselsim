# -*- mode: python; coding: utf-8; -*-

from migselsim.baseplugin import PluginMount

class CommandPluginMount(PluginMount):
        """
    Parental class of all command plugins.

    All plugins inherited from this class are registered in CommandPluginMount dict.
    """
    pass


class CommandPlugin(object):
    """
    Mount point for sub-level commands plugins.

    Plugins implementing this interface should provide the following attributes:

    :key:   Command name.

    :execute:  Code for a command.

    """
    __metaclass__ = CommandPluginMount

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
            raise ValueError

    def execute(self, value, parent, simulator):
        raise NotImplementedError
