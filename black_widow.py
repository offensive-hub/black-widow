#!/usr/bin/env python3
# coding=utf-8

"""
****************************   🕷️  Black-Widow  🕷️   *****************************
*                                                                               *
* black_widow.py -- Main black-widow file.                                      *
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

from . import app

import os
import sys


class AppType:
    CMD = 'CMD'
    GUI = 'GUI'


def make_temp_dir():
    app.helpers.storage.check_folder(app.env.APP_TMP)
    try:
        app.helpers.storage.chmod(app.env.APP_TMP, 0o0777, True)
    except PermissionError:
        pass


# Startup
def init(app_type):
    make_temp_dir()
    app.services.Log.info(app.env.APP_NAME + ' ' + str(app_type) + ' started, PID=' + str(os.getpid()))
    app.services.Log.info('DEBUG is ' + str(app.env.APP_DEBUG))


# Main function for TEST app
def main_test():
    init(AppType.CMD)
    ip = app.helpers.network.get_ip_address()
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
        app.services.Log.info('Django manager executed')
        app.services.Log.info('Django arguments: ' + str(django_args))
        app.gui.django_cmd(django_args)
        sys.exit(0)

    elif arguments.pcap:
        if arguments.pcap_int is None:
            print("\nSpecify at least one interface (eg. --pcap-int=wlan0)\n")
            sys.exit(1)
        app.managers.sniffer.PcapSniffer.sniff(src_file=arguments.pcap_src, interfaces=arguments.pcap_int,
                                               dest_file=arguments.pcap_dest, filters=arguments.pcap_filters,
                                               limit_length=arguments.pcap_limit, pkt_count=arguments.pcap_count,
                                               callback=None)
    elif arguments.sql:
        if arguments.sql_url is None:
            print('Specify an url! (eg. --sql-url=https://black-widow.io)\n')
            sys.exit(1)
        if not app.helpers.validators.is_url(arguments.sql_url):
            print('"' + arguments.sql_url + '" is not a valid URL!\n')
            sys.exit(1)
        app.managers.injection.SqlInjection.inject(
            arguments.sql_forms,
            arguments.sql_url,
            arguments.sql_depth,
            True
        )
    elif arguments.crawl:
        if arguments.crawl_url is None:
            print('Specify an url! (eg. --crawl-url=https://black-widow.io)\n')
            sys.exit(1)
        if not app.helpers.validators.is_url(arguments.crawl_url):
            print('"' + arguments.crawl_url + '" is not a valid URL!\n')
            sys.exit(1)
        crawl_types = app.managers.parser.HtmlParser.types()
        if arguments.crawl_type not in crawl_types:
            print('Specify a crawling type! (eg. --crawl-type=form_parse)\n')
            print('Accepted types:')
            type_desc = app.managers.parser.HtmlParser.type_descriptions()
            for crawl_type in crawl_types:
                print('    - ' + crawl_type + ' (' + type_desc[crawl_type] + ')')
            print('')
            sys.exit(1)
        app.managers.parser.HtmlParser.crawl(
            arguments.crawl_url,
            arguments.crawl_type,
            app.managers.parser.HtmlParser.print_parsed,
            arguments.crawl_depth
        )


# Main function generic app
def main():
    arguments = app.arguments.get_arguments()
    if arguments.gui:
        main_gui()
    else:
        main_cmd(arguments)
