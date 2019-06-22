import argparse, sys, copy

def _callable(obj):
    return hasattr(obj, '__call__') or hasattr(obj, '__bases__')

def get_spaced_line(line, depth=0):
    if (type(line) == str): return (' '*depth) + str(line)
    return line

# Better prefix
class _CapitalisedHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None: prefix = 'Usage: '
        return super(_CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)

    def _add_item(self, func, args):
        self._current_section.items.append((func, args))

    def add_argument(self, action, depth=0):
        option_strings = copy.deepcopy(action.option_strings)
        action.option_strings.clear()
        for option_string in option_strings:
            action.option_strings.append((' '*depth) + option_string)

        if action.help is not argparse.SUPPRESS:

            # find all invocations
            get_invocation = self._format_action_invocation
            invocations = [get_invocation(action)]
            for subaction in self._iter_indented_subactions(action):
                invocations.append(get_invocation(subaction))

            # update the maximum item length
            invocation_length = max([len(s) for s in invocations])
            action_length = invocation_length + self._current_indent
            self._action_max_length = max(self._action_max_length,
                                          action_length)

            # add the item to the list
            self._add_item(self._format_action, [action])

    def add_arguments(self, actions, depth=0):
        for action in actions:
            self.add_argument(action, depth)

# Extension of argparse.ArgumentParser class, that allows better subgroup managing
class ArgumentParser(argparse.ArgumentParser):
    """
    Keyword Arguments:
        - prog -- The name of the program (default: sys.argv[0])
        - usage -- A usage message (default: auto-generated from arguments)
        - description -- A description of what the program does
        - epilog -- Text following the argument descriptions
        - parents -- Parsers whose arguments should be copied into this one
        - formatter_class -- HelpFormatter class for printing help messages
        - prefix_chars -- Characters that prefix optional arguments
        - fromfile_prefix_chars -- Characters that prefix files containing
            additional arguments
        - argument_default -- The default value for all arguments
        - conflict_handler -- String indicating how to handle conflicts
        - add_help -- Add a -h/-help option
    """

    def __init__(self,
                 prog=None,
                 usage=sys.argv[0]+' [Options]',
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

    # Overwrite Parent.print_usage
    # Preventing that print_help prints two times the usage output
    def print_usage(self, output): return

    # Overwrite Parent.format_help
    def format_help(self, depth=0):
        formatter = self._get_formatter()

        # usage
        formatter.add_usage(self.usage, self._actions,
                            self._mutually_exclusive_groups)

        # description
        formatter.add_text(self.description)

        # positionals, optionals and user-defined groups
        ArgumentParser.fill_formatter(self, formatter, depth)

        # epilog
        formatter.add_text(get_spaced_line(self.epilog, depth))

        # determine help from format above
        formatted_help = formatter.format_help()

        return formatter.format_help()

    @staticmethod
    def fill_formatter(argument, formatter, depth=0):
        actions = argument._action_groups
        if (hasattr(argument, '_group_actions')): actions += argument._group_actions

        section_loop = not hasattr(argument, 'title')
        if (not section_loop): formatter.start_section(get_spaced_line(argument.title, depth))

        for action_group in actions:

            if (section_loop):
                start = action_group.title
                text = action_group.description
                formatter.start_section(get_spaced_line(start, depth))
                formatter.add_text(get_spaced_line(text, depth))
            else:
                start = ', '.join(action_group.option_strings)
                formatter.add_argument(action_group, depth=depth)

            if (hasattr(action_group, '_group_actions')):
                formatter.add_arguments(action_group._group_actions, depth=depth)

            if (hasattr(action_group, '_action_groups')):
                for child_action_group in action_group._action_groups:
                    if (type(child_action_group) == argparse._ArgumentGroup):
                        ArgumentParser.fill_formatter(child_action_group, formatter, depth)

            if (section_loop): formatter.end_section()

        if (not section_loop): formatter.end_section()
