"""
*********************************************************************************
*                                                                               *
* input_arguments.py -- Methods to parse the user input arguments.              *
*                                                                               *
********************** IMPORTANT BLACK-WIDOW LICENSE TERMS **********************
*                                                                               *
* This file is part of black-widow.                                             *
*                                                                               *
* black-widow is free software: you can redistribute it and/or modify           *
* it under the terms of the GNU General Public License as published by          *
* the Free Software Foundation, either version 3 of the License, or             *
* (at your option) any later version.                                           *
*                                                                               *
* black-widow is distributed in the hope that it will be useful,                *
* but WITHOUT ANY WARRANTY; without even the implied warranty of                *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 *
* GNU General Public License for more details.                                  *
*                                                                               *
* You should have received a copy of the GNU General Public License             *
* along with black-widow.  If not, see <http://www.gnu.org/licenses/>.          *
*                                                                               *
*********************************************************************************
"""

import sys
import argparse

from black_widow import app


def create_parser():
    """
    Set the expected arguments
    :return: The created ArgumentParser
    """
    # --- Parser ---#
    parser = ArgumentParser(usage=sys.argv[0] + ' [Options]')

    # --- Options ---#
    options = parser.add_argument_group("Options")
    options.add_argument("-h", "--help", help="Show this help message and exit",
                         action="store_true")
    options.add_argument("-v", "--version", help="Show program's version number and exit",
                         action="store_true")
    # options.add_argument("-t", "--test", help="Execute a test",
    #                      action="store_true")
    options.add_argument("-g", "--gui", help="Run " + app.env.APP_NAME + " with GUI",
                         action="store_true")
    options.add_argument("--django", help="Run django manager (eg. `--django 'help'`)",
                         type=str, metavar='ARGS')

    # Packet Sniffing
    options_pcap = options.add_argument_group("Sniffing")
    options_pcap.add_argument("--pcap", help="Sniff Packages", action="store_true")
    options_pcap.add_argument("--pcap-src", help="The .pcap source file", type=argparse.FileType('r'),
                              metavar='FILE')
    options_pcap.add_argument("--pcap-dest", help="The .pcap destination file",
                              type=argparse.FileType('w'), metavar='FILE')
    options_pcap.add_argument("--pcap-int", help="Network interfaces (eg: eth0,wlan0)", type=str, metavar='INTERFACES')
    options_pcap.add_argument("--pcap-filters", help="https://wiki.wireshark.org/CaptureFilters", type=str,
                              metavar='FILTERS')
    options_pcap.add_argument("--pcap-limit", help="Max field lengths of each packet", type=int, metavar='INTEGER')
    options_pcap.add_argument("--pcap-count", help="Max packets to sniff", type=int, metavar='INTEGER')

    # Web Parsing
    crawl_types = '|'.join(app.managers.parser.HtmlParser.types())
    options_sql = options.add_argument_group("Web Parsing")
    options_sql.add_argument("--crawl", help="Crawl a website", action="store_true")
    options_sql.add_argument("--crawl-url", help="The url to crawl", type=str, metavar='URL')
    options_sql.add_argument("--crawl-type", help=crawl_types, type=str, metavar='TYPE')
    options_sql.add_argument("--crawl-depth", help="The crawl depth", type=int, metavar='INTEGER', default=0)

    # SQL Injection
    options_sql = options.add_argument_group("SQL Injection")
    options_sql.add_argument("--sql", help="Try injection in a website", action="store_true")
    options_sql.add_argument("--sql-url", help="The url where search for forms or to inject", type=str, metavar='URL')
    options_sql.add_argument("--sql-depth", help="Max crawling depth", type=int, metavar='INTEGER', default=0)
    options_sql.add_argument("--sql-forms", help="Parse the forms on page", action="store_true")

    return parser


# Creates the argument parser and return the parsed input arguments
def get_arguments():
    """
    Get the CLI arguments
    :return: dict The arguments
    """
    # --- Header image ---#
    def print_header():
        """
        Print the software header
        """
        header_ascii = app.helpers.storage.read_file(
            app.env.RES_PATH + '/' + str(app.env.APP_PROC) + '-ascii.txt'
        )
        header_ascii = header_ascii.replace('{version}', app.env.APP_VERSION)
        print('\n' + header_ascii + '\n')

    parser = create_parser()
    args = parser.parse_args()

    if args.version:
        print(app.env.APP_VERSION)
        sys.exit(0)

    print_header()

    # Check if at least one argument is set
    arg_set = False
    # noinspection PyProtectedMember
    for arg in args._get_kwargs():
        arg_set = arg[1] or arg_set
    if args.help or not arg_set:
        # Print help
        parser.print_help()
        print()  # print newline
        sys.exit(0)

    return args


def get_spaced_line(line, depth=0):
    """
    Prepend a line with certain space
    :param line: the line to edit
    :param depth: the number of spaces to insert
    :return: the prepended line
    """
    if type(line) == str:
        return (' ' * depth) + str(line)
    return line


class _CapitalisedHelpFormatter(argparse.HelpFormatter):

    # max_help_position
    def __init__(self, prog, indent_increment=2, max_help_position=36, width=None):
        argparse.HelpFormatter.__init__(self, prog, indent_increment, max_help_position, width)

    # CamelCase prefix
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(_CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)

    # Added depth
    def add_argument(self, action, depth=0):
        option_strings = []
        for option_string in action.option_strings:
            option_strings.append((' ' * depth) + option_string)
        action.option_strings = option_strings
        argparse.HelpFormatter.add_argument(self, action)

    # Added depth
    def add_arguments(self, actions, depth=0):
        for action in actions:
            self.add_argument(action, depth)


# Better subgroup managing (with depth)
class ArgumentParser(argparse.ArgumentParser):
    # noinspection PyDefaultArgument
    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=_CapitalisedHelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=False):
        argparse.ArgumentParser.__init__(self,
                                         prog=prog,
                                         usage=usage,
                                         description=description,
                                         epilog=epilog,
                                         # version=version,     # unexpected keyword (?!)
                                         parents=parents,
                                         formatter_class=formatter_class,
                                         prefix_chars=prefix_chars,
                                         fromfile_prefix_chars=fromfile_prefix_chars,
                                         argument_default=argument_default,
                                         conflict_handler=conflict_handler,
                                         add_help=add_help)

    # Overwrite Parent.format_help
    def format_help(self, depth=0):
        formatter = self._get_formatter()

        # usage
        formatter.add_usage(self.usage, self._actions,
                            self._mutually_exclusive_groups)

        # description
        formatter.add_text(self.description)

        # positionals, optionals and user-defined groups
        # new recursive method to manage subgroups
        ArgumentParser.fill_formatter(self, formatter, depth)

        # epilog
        formatter.add_text(get_spaced_line(self.epilog, depth))

        return formatter.format_help()

    # noinspection PyProtectedMember
    @staticmethod
    def fill_formatter(argument, formatter, depth=0):
        """
        Manage correctly the subgroups depth
        :param argument: The argument to format
        :param formatter: The formatter to fill
        :param depth: The initial depth of the printed params
        """
        actions = argument._action_groups
        if hasattr(argument, '_group_actions'):
            actions += argument._group_actions

        # print(type(argument))

        if type(argument) == ArgumentParser:
            subsections = True
        else:
            subsections = False
            formatter.start_section(get_spaced_line(argument.title, depth))

        for action_group in actions:
            if subsections:
                formatter.start_section(get_spaced_line(action_group.title, depth))
                formatter.add_text(get_spaced_line(action_group.description, depth))
                formatter.add_arguments(action_group._group_actions, depth=depth)
                for child_action_group in action_group._action_groups:
                    if type(child_action_group) == argparse._ArgumentGroup:
                        ArgumentParser.fill_formatter(child_action_group, formatter, depth)
            else:
                formatter.add_argument(action_group, depth=depth)

            if subsections:
                formatter.end_section()

        if not subsections:
            formatter.end_section()
