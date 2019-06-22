#!/usr/bin/env python3

import os, sys, getopt, lib, app

VERSION = '1.0.0#alpha'


class AppType:
    CMD=''
    GUI='GUI'


class CapitalisedHelpFormatter(lib.args.argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None: prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
        usage, actions, groups, prefix)

# Creates the argument parser and return the parsed input arguments
def get_arguments():
    #--- Header image ---#
    def print_header():
        header_ascii = app.utils.helpers.storage.read_file(app.env.RES_PATH+'/' + str(app.env.APP_PROC) + '-ascii.txt')
        header_ascii = header_ascii.replace('{version}', VERSION)
        print('\n' + header_ascii + '\n')

    #--- Parser ---#
    parser = lib.args.Arguments()
    print(dir(parser))
    exit(0)

    #--- Options ---#
    options = parser.add_argument_group("General Options")
    options.add_argument("-h", "--help", help="Show this help message and exit",
                         action="store_true")
    options.add_argument("-v", "--version", help="Show program's version number and exit",
                         action="store_true")

    options_pcap = parser.add_argument_group("Sniffing Options")
    options_pcap.add_argument("--sniff", help="Sniff Packages", type=str, metavar='FILTERS')

    options_sql = parser.add_argument_group("SQL Options")
    options_sql.add_argument("--sql", help="Try injection in a website. Avilable settings: url=https://example.com deep=true", type=str, metavar='[SETTINGS]')

    print(dir(options))
    exit(0)

    try:
        args = parser.parse_args()
    except:
        app.utils.helpers.logger.Log.error("Unrecognized arguments exception")
        print_header()
        parser.print_help()
        print()
        parser.exit(2)

    if (args.version):
        print(VERSION)
        parser.exit(0)

    print_header()

    # Check if at least one argument is set
    arg_set = False
    for arg in args._get_kwargs(): arg_set = arg[1] or arg_set
    if (args.help or not arg_set):
        # Print help
        parser.print_help()
        print()
        parser.exit(0)

    global usage
    usage = parser.print_help

    return args

# Startup
def boot(app_type):
    app.utils.helpers.logger.Log.info(app.env.APP_NAME+' '+str(app_type)+' GUI started, PID='+str(os.getpid()))


# Main function for GUI app
def main_gui():
    boot(AppType.GUI)
    app.gui.main.open()


# Main function for command line app
def main_cmd():
    boot(AppType.CMD)


# Main function generic app
def main():
    arguments = get_arguments()
    # TODO: ask interface, [dest_file], [filter]
    if (arguments.sniff):
        import pprint
        def pcap_callback(pkt_dict):
            pprint.pprint(pkt_dict)
    #app.utils.sniffing.sniff_pcap(src_file=None, interface=interface, dest_file=test_pcap_out, filter=filter7, limit_length=10000, callback=pcap_callback)
    return()

if __name__ == "__main__":
    main()
