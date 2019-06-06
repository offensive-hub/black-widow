#!/usr/bin/env python3

import os, sys, getopt, argparse, app

VERSION = '1.0.0#alpha'

class AppType:
    CMD=''
    GUI='GUI'

class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None: prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
        usage, actions, groups, prefix)

def usage():
    #--- Custom print_usage ---#
    def print_usage(output): return

    #--- Header image ---#
    def print_header():
        header_ascii = app.utils.helpers.storage.read_file(app.env.RES_PATH+'/' + str(app.env.APP_PROC) + '-ascii.txt')
        header_ascii = header_ascii.replace('{version}', VERSION)
        print('\n' + header_ascii + '\n')

    #--- Usage ---#
    parser = argparse.ArgumentParser(add_help=False, usage=sys.argv[0]+' [Options]', formatter_class=CapitalisedHelpFormatter)
    parser.print_usage = print_usage   # Already printed with print_help

    #--- Options ---#
    options = parser.add_argument_group("Options")
    options.add_argument("-h", "--help", help="Show this help message and exit",
                         action="store_true")
    #options.add_argument("-v", "--verbose", help="Increase output verbosity",
    #                     action="store_true")
    options.add_argument("-v", "--version", help="Show program's version number and exit",
                         action="store_true")


    options_pcap = options.add_argument_group("Sniffing")
    options_pcap.add_argument("--sniff", help="Sniff Packages", type=str, metavar='[FILTERS]')

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

    if (args.help):
        parser.print_help()
        print()
        parser.exit(0)

    # TODO: ask interface, [dest_file], [filter]
    if (args.sniff):
        import pprint
        def pcap_callback(pkt_dict):
            pprint.pprint(pkt_dict)
    #app.utils.sniffing.sniff_pcap(src_file=None, interface=interface, dest_file=test_pcap_out, filter=filter7, limit_length=10000, callback=pcap_callback)

    print()

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
    usage()
    return()
    try:
        args = sys.argv[1:]
        opts, args = getopt.getopt(args, "hi:o:", ["ifile=", "ofile="])
        print('opts:')
        print(opts)
        print('args:')
        print(args)
        print('---------')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    return
    inputfile = ''
    outputfile = ''
    print(opts)
    for opt, arg in opts:
        print(opt)
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print ('Input file is ' + inputfile)
    print ('Output file is ' + outputfile)


if __name__ == "__main__":
    main()
