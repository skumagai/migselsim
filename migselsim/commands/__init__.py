# -*- mode: python; coding: utf-8; -*-

from argparse import ArgumentParser

from migselsim.baseplugin import PluginMount
from migselsim.definition import COMMAND, VERSION

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

    :name: command name

    :description: short summary of commands

    :usage: usage of command

    :execute: code for a command

    """

    name = None
    description = ''
    usage = None

    __metaclass__ = CommandPluginMount

    def __init__(self):
        self.parser = ArgumentParser(usage = self.usage,
                                     prog = '{} {}'.format(COMMAND, self.name))

    def execute(self, value, parent, simulator):
        raise NotImplementedError


def list_all_commands():
    return CommandPlugin.plugins
