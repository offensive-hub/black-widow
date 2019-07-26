import os
import sys

from gunicorn.app.wsgiapp import run as gunicorn_run
from django.core import management

from app.env_local import APP_WEB_HOST, APP_WEB_PORT
from app.env import EXEC_PATH, APP_NAME
from app.utils.helpers import multithread, multiprocess
from app.utils.helpers.logger import Log
from app.utils.helpers.network import get_ip_address
from app.gui.web.wsgi import WEB_PACKAGE


def _get_bind_socket():
    host = APP_WEB_HOST
    if host is None:
        host = get_ip_address()
    if host is None:
        host = '0.0.0.0'
    return str(host) + ':' + str(APP_WEB_PORT)


def django_gui():
    # Go to "/app/gui/" directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    # sys.path.insert(0, os.path.dirname(__file__))
    bind_host = _get_bind_socket()
    Log.info("Starting " + str(APP_NAME) + ' GUI')
    sys.argv = [sys.argv[0], 'web.wsgi', '-b', bind_host]
    multiprocess(gunicorn_run, (), True, 1)
    Log.success("Started " + str(APP_NAME) + ' GUI')


def django_cmd(args):
    # Go to "web" directory
    if 'runserver' not in args:
        os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'web'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", WEB_PACKAGE + ".settings")
    management.execute_from_command_line([EXEC_PATH + ' --django', ] + args)
