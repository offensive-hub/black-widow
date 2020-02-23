"""
*********************************************************************************
*                                                                               *
* manage.py -- Django manager.                                                  *
*                                                                               *
* Methods to use the Django manager to test the web server                      *
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

import os
import sys
import webbrowser

from gunicorn.app.wsgiapp import run as gunicorn_run
from django.core import management

from black_widow.app.env import EXEC_PATH, APP_NAME, APP_WEB_HOST, APP_WEB_PORT
from black_widow.app.services import MultiTask, Log
from black_widow.app.helpers.network import get_ip_address
from black_widow.app.helpers.storage import delete
from black_widow.app.helpers.util import whoami, set_owner_process
from black_widow.app.gui.web.wsgi import WEB_PACKAGE


def django_gui():
    sys.path.insert(0, os.path.dirname(__file__))
    bind_host = _get_bind_socket()
    Log.info("Starting " + str(APP_NAME) + ' GUI')
    sys.argv = [sys.argv[0], 'web.wsgi', '-b', bind_host]
    django_cmd(['migrate'])
    _launch_browser(bind_host)
    gunicorn_run()


def django_cmd(args: list):
    if 'runserver' not in args:
        # cd to "web" directory
        os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'web'))
    elif len(args) <= 1:
        bind_host = _get_bind_socket()
        args.append(bind_host)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", WEB_PACKAGE + ".settings")
    management.execute_from_command_line([EXEC_PATH + ' --django', ] + args)


def _launch_browser(bind_host: str):
    user = whoami()

    def browser_target():
        """
        The function that launch the browser
        """
        set_owner_process(user)
        Log.info('Launching browser with User: ' + str(whoami(False)))
        webbrowser.open('http://' + bind_host)
        Log.success('Web browser opened')

    pidfile = MultiTask.multiprocess(browser_target, asynchronous=True, cpu=1)
    delete(pidfile)     # The pidfile is not required


def _get_bind_socket():
    host = APP_WEB_HOST
    if host is None:
        host = get_ip_address()
    if host is None:
        host = '0.0.0.0'
    return str(host) + ':' + str(APP_WEB_PORT)
