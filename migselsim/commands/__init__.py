# -*- mode: python; coding: utf-8; -*-
import os

from migselsim.baseplugin import PluginMount, Plugin

class CommandPluginMount(PluginMount):
    """
    Parental class of all command plugins.

    All plugins inherited from this class are registered in CommandPluginMount dict.
    """
    pass


class CommandPlugin(Plugin):
    """
    Baseclass of subcommand plugins.

    Plugins implementing this interface should provide the following attributes:

    :key: command name

    :description: short summary of commands

    :usage: usage of command

    :execute: code for a command

    """

    __metaclass__ = CommandPluginMount

    @staticmethod
    def execute(*args):
        raise NotImplementedError
