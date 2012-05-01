# -*- mode: python; coding: utf-8; -*-

from migselsim.commands import CommandPlugin
from migselsim.baseparser import command_parsers, parser

class Help(CommandPlugin):
    """Print help messages."""
    key = 'help'
    description = 'print help messages of available commands'
    subparser = command_parsers.add_parser(key, help = description)
    subparser.add_argument('target', nargs='?',
                           default='all',
                           metavar='command')

    def execute(self, args):

        if args.target.lower() == 'all':
            # default case: print help of all commands.
            parser.print_help()
            return

        if args.target not in CommandPlugin.plugins:
            parser.error('Unkown command: `{}`'.format(args.target))
            return

        parser.parse_args([args.target, '--help'])
