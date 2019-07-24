import os
import webbrowser

# from django import setup as django_setup
from django.core import management
from django.core.servers.basehttp import simple_server

from app.env_local import APP_WEB_HOST, APP_WEB_PORT
from app.env import EXEC_PATH
from app.utils.helpers.logger import Log
from app.utils.helpers.network import get_ip_address
from app.utils.helpers.multitask import multithread, multiprocess
from app.gui.web.wsgi import WEB_PACKAGE
from app.gui.web.wsgi import application


def _get_preferred_ip():
    host = APP_WEB_HOST
    if host is None:
        host = get_ip_address()
    if host is None:
        host = '0.0.0.0'
    return host


def django_gui():
    host = _get_preferred_ip()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", WEB_PACKAGE + ".settings")

    print("Starting the django web-server in a parallel thread")

    pid = os.fork()
    if pid == 0:
        print("Django web-server PID: {}".format(os.getpid()))
        # django_setup()
        django_server = simple_server.make_server(host, APP_WEB_PORT, application)
        django_server.serve_forever()
        Log.success("Started the django web-server in parallel thread!")
        # management.call_command('runserver', '--noreload')
        exit(0)

    print("Django web-server started!")
    print("Host: " + str(host))
    print("Port: " + str(APP_WEB_PORT))
    webbrowser.open(host + ':' + str(APP_WEB_PORT), new=2)
    exit(0)


def django_cmd(args):
    # Go to "web" directory
    if 'runserver' not in args:
        os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'web'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", WEB_PACKAGE + ".settings")
    management.execute_from_command_line([EXEC_PATH + ' --django', ] + args)
