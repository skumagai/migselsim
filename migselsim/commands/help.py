# -*- mode: python; coding: utf-8; -*-

from migselsim.commands import CommandPlugin, list_all_commands
from migselsim.baseparser import command_parsers

class Help(CommandPlugin):
    """Print help messages."""
    key = 'help'
    description = 'print help messages of available commands'

    def execute(self, options, args):
        pass
        # if args:
        #     # display help message for a signle command
        #     command = args[0]
        #     if command not in list_all_commands:
        #         parser.error("Unkown command: `{}`".format(command))
        #     else:
        #         command = list_all_commands[command]
        #         command.parser.print_help()
        # else:
        #     # display short descriptions of all avaialbe commands
        #     parser.print_help()
        #     print("\nAvailable commands:")
        #     for command in list_all_commands():
        #         print("  {}: {}".format(command.name, command.description))
