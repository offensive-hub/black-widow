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
    options_pcap.add_argument("--pcap-src", help="The .pcap source file", type=str, metavar='FILE')
    options_pcap.add_argument("--pcap-dest", help="The .pcap destination file", type=str, metavar='FILE')
    options_pcap.add_argument("--pcap-int", help="Network interface (ex: eth0)", type=str, metavar='INTERFACE')
    options_pcap.add_argument("--pcap-filters", help="https://wiki.wireshark.org/CaptureFilters", type=str, metavar='FILTERS')

    # SQL Injection
    options_sql = options.add_argument_group("SQL Injection")
    options_sql.add_argument("--sql", help="Try injection in a website", action="store_true")
    options_sql.add_argument("--sql-url", help="The url where search for forms", type=str,  metavar='URL')
    options_sql.add_argument("--sql-deep", help="Crawl the website", choices=['1', '0'])

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
def init(app_type):
    app.utils.helpers.logger.Log.info(app.env.APP_NAME+' '+str(app_type)+' GUI started, PID='+str(os.getpid()))


# Main function for GUI app
def main_gui():
    init(AppType.GUI)
    # Ignore arguments
    app.gui.main.open()


# Main function for command line app
def main_cmd():
    init(AppType.CMD)
    if (arguments.sniff):
        import pprint
        def pcap_callback(pkt_dict):
            pprint.pprint(pkt_dict)
        app.utils.sniffing.sniff_pcap(src_file=None, interface=interface, dest_file=test_pcap_out, filter=filter, limit_length=10000, callback=pcap_callback)


# Main function generic app
def main():
    arguments = get_arguments()
    if (not arguments.gui): main_cmd()
    else: main_gui()
    return()

if __name__ == "__main__":
    main()
