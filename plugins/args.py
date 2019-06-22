import argparse

# Prepend the space
# @param depth The number of spaces to insert
def get_spaced_line(line, depth=0):
    if (type(line) == str): return (' '*depth) + str(line)
    return line


# @class _CapitalisedHelpFormatter Extension of argparse.HelpFormatter
class _CapitalisedHelpFormatter(argparse.HelpFormatter):

    # max_help_position
    def __init__(self, prog, indent_increment=2, max_help_position=36, width=None):
        argparse.HelpFormatter.__init__(self, prog, indent_increment, max_help_position, width)

    # CamelCase prefix
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None: prefix = 'Usage: '
        return super(_CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)

    # Added depth
    def add_argument(self, action, depth=0):
        option_strings = []
        for option_string in action.option_strings:
            option_strings.append((' '*depth) + option_string)
        action.option_strings = option_strings
        argparse.HelpFormatter.add_argument(self, action)

    # Added depth
    def add_arguments(self, actions, depth=0):
        for action in actions: self.add_argument(action, depth)


# Better subgroup managing (with depth)
# @class ArgumentParser Extension of argparse.ArgumentParser
class ArgumentParser(argparse.ArgumentParser):
    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 version=None,
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

        # determine help from format above
        formatted_help = formatter.format_help()

        return formatter.format_help()

    # Manage correctly the subgroups depth
    # @method fill_formatter
    @staticmethod
    def fill_formatter(argument, formatter, depth=0):
        actions = argument._action_groups
        if (hasattr(argument, '_group_actions')): actions += argument._group_actions

        #print(type(argument))

        if (type(argument) == ArgumentParser):
            subsections = True
        else:
            subsections = False
            formatter.start_section(get_spaced_line(argument.title, depth))

        for action_group in actions:
            if (subsections):
                formatter.start_section(get_spaced_line(action_group.title, depth))
                formatter.add_text(get_spaced_line(action_group.description, depth))
                formatter.add_arguments(action_group._group_actions, depth=depth)
                for child_action_group in action_group._action_groups:
                    if (type(child_action_group) == argparse._ArgumentGroup):
                        ArgumentParser.fill_formatter(child_action_group, formatter, depth)
            else:
                formatter.add_argument(action_group, depth=depth)

            if (subsections): formatter.end_section()

        if (not subsections): formatter.end_section()
