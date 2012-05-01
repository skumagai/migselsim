# -*- mode: python; coding: utf-8; -*-
import os

from migselsim.baseplugin import PluginMount, Plugin
from migselsim.definition import COMMAND, VERSION

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

    key = None
    description = ''
    usage = None

    __metaclass__ = CommandPluginMount

    def execute(self, value, parent, simulator):
        raise NotImplementedError


def list_all_commands():
    # for path in __path__:
    #     for module in [m[:-3] for m in os.listdir(path)]
    CommandPlugin.scan()
    return {key: value() for key, value in CommandPlugin.plugins.iteritems()}

all_commands = list_all_commands()
