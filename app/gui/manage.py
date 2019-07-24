import os
import webbrowser

from django import setup as django_setup
from django.core import management

from app.env_local import APP_WEB_HOST, APP_WEB_PORT
from app.env import EXEC_PATH
from app.utils.helpers.logger import Log
from app.utils.helpers.network import get_ip_address
from app.utils.helpers.multitask import multithread
from app.gui.web.settings import WEB_PACKAGE


def _get_preferred_ip():
    host = APP_WEB_HOST
    if host is None:
        host = get_ip_address()
    if host is None:
        host = '0.0.0.0'
    return host


def django_gui():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", WEB_PACKAGE + ".settings")

    Log.info("Starting the django web-server in a parallel thread")
    django_setup()
    multithread(management.call_command, ('runserver', '--noreload'), True, 1)
    Log.success("Django web-server started!")

    host = _get_preferred_ip()
    Log.info("Host: " + str(host))
    Log.info("Port: " + str(APP_WEB_PORT))

    webbrowser.open(host + ':' + str(APP_WEB_PORT), new=2)


def django_cmd(args):
    # Go to "web" directory
    if 'runserver' not in args:
        os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'web'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", WEB_PACKAGE + ".settings")
    management.execute_from_command_line([EXEC_PATH + ' --django', ] + args)
