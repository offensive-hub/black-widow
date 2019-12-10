#!/usr/bin/env python3
# coding=utf-8

"""
****************************   🕷️  Black-Widow  🕷️   ****************************
*                                                                               *
* black-widow.py -- Main black-widow executable.                                *
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

import app
import os
import sys

from app_plugins import args


class AppType:
    CMD = 'CMD'
    GUI = 'GUI'


# Startup
def init(app_type):
    app.utils.helpers.logger.Log.info(app.env.APP_NAME + ' ' + str(app_type) + ' started, PID=' + str(os.getpid()))
    app.utils.helpers.logger.Log.info('DEBUG is ' + str(app.env_local.APP_DEBUG))


# Main function for TEST app
def main_test():
    init(AppType.CMD)
    ip = app.utils.helpers.network.get_ip_address()
    print('ip: ' + str(ip))


# Main function for GUI app
def main_gui():
    init(AppType.GUI)
    app.gui.django_gui()


# Main function for command line app
def main_cmd(arguments):
    init(AppType.CMD)
    if arguments.django:
        django_args = str.split(arguments.django)
        app.utils.helpers.logger.Log.info('Django manager executed')
        app.utils.helpers.logger.Log.info('Django arguments: ' + str(django_args))
        app.gui.django_cmd(django_args)
        sys.exit(0)

    elif arguments.pcap:
        if arguments.pcap_int is None:
            print('Please, specify an interface! (eg. --pcap-int=wlan0)\n')
            sys.exit(1)
        app.utils.sniffing.sniff_pcap(src_file=arguments.pcap_src, interface=arguments.pcap_int,
                                      dest_file=arguments.pcap_dest, filters=arguments.pcap_filters,
                                      limit_length=arguments.pcap_limit)
    elif arguments.sql:
        if arguments.sql_url is None:
            print('Please, specify an url! (eg. --sql-url=https://black-widow.io)\n')
            sys.exit(1)
        if arguments.sql_deep:
            app.utils.sql.deep_inject_form(arguments.sql_url, arguments.sql_depth)
        else:
            app.utils.sql.inject_form(arguments.sql_url)


# Main function generic app
def main():
    if not app.utils.helpers.util.is_root():
        print("Root privileges required to run " + app.env.APP_PROC + "!\n")
        sys.exit(50)
    arguments = args.get_arguments()
    if arguments.gui:
        main_gui()
    elif arguments.test:
        main_test()
    else:
        main_cmd(arguments)


if __name__ == "__main__":
    main()
