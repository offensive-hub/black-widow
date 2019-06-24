#!/usr/bin/env python3

import os, sys, getopt, plugins, app

VERSION = '1.0.0#alpha'


class AppType:
    CMD='CMD'
    GUI='GUI'

# Creates the argument parser and return the parsed input arguments
def get_arguments():
    #--- Header image ---#
    def print_header():
        header_ascii = app.utils.helpers.storage.read_file(app.env.RES_PATH+'/' + str(app.env.APP_PROC) + '-ascii.txt')
        header_ascii = header_ascii.replace('{version}', VERSION)
        print('\n' + header_ascii + '\n')

    #--- Parser ---#
    parser = plugins.args.ArgumentParser(usage=sys.argv[0]+' [Options]')

    #--- Options ---#
    options = parser.add_argument_group("Options")
    options.add_argument("-h", "--help", help="Show this help message and exit",
                         action="store_true")
    options.add_argument("-v", "--version", help="Show program's version number and exit",
                         action="store_true")
    options.add_argument("-g", "--gui", help="Run "+app.env.APP_NAME+" with GUI",
                         action="store_true")

    # Sniffing
    options_pcap = options.add_argument_group("Sniffing")
    options_pcap.add_argument("--sniff", help="Sniff Packages", action="store_true")
    options_pcap.add_argument("--pcap-src", help="The .pcap source file", type=plugins.args.argparse.FileType('r'), metavar='FILE')
    options_pcap.add_argument("--pcap-dest", help="The .pcap destination file", type=plugins.args.argparse.FileType('w'), metavar='FILE')
    options_pcap.add_argument("--pcap-int", help="Network interface (ex: eth0)", type=str, metavar='INTERFACE')
    options_pcap.add_argument("--pcap-filters", help="https://wiki.wireshark.org/CaptureFilters", type=str, metavar='FILTERS')
    options_pcap.add_argument("--pcap-limit", help="Max field lengths of each packet", type=int, metavar='INTEGER')

    # SQL Injection
    options_sql = options.add_argument_group("SQL Injection")
    options_sql.add_argument("--sql", help="Try injection in a website", action="store_true")
    options_sql.add_argument("--sql-deep", help="Crawl the website in search for forms", action="store_true")
    options_sql.add_argument("--sql-url", help="The url where search for forms", type=str,  metavar='URL')

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
        print() # print newline
        parser.exit(0)

    global usage
    usage = parser.print_help

    return args


# Startup
def init(app_type):
    app.utils.helpers.logger.Log.info(app.env.APP_NAME+' '+str(app_type)+' started, PID='+str(os.getpid()))


# Main function for GUI app
def main_gui(arguments):
    init(AppType.GUI)
    # Ignore arguments
    app.gui.main.open()


# Main function for command line app
def main_cmd(arguments):
    init(AppType.CMD)
    if (arguments.sniff):
        if (arguments.pcap_int == None):
            print('Please, specific an interface! (ex. --pcap-int=wlan0)\n');
            sys.exit(1)
        if (arguments.pcap_src != None): src_file = arguments.pcap_src.name
        else: src_file = None
        if (arguments.pcap_dest != None): dest_file = arguments.pcap_dest.name
        else: dest_file = None
        limit_length=2000  # The max package fields length (the bigger fields will be truncated)
        app.utils.sniffing.sniff_pcap(src_file=src_file, interface=arguments.pcap_int, dest_file=dest_file, filter=arguments.pcap_filters, limit_length=arguments.pcap_limit)


# Main function generic app
def main():
    arguments = get_arguments()
    if (not arguments.gui): main_cmd(arguments)
    else: main_gui(arguments)

if __name__ == "__main__":
    main()
