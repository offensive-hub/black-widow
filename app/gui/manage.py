import os
import webbrowser

from django.core.servers.basehttp import simple_server

from app.env_local import APP_WEB_HOST, APP_WEB_PORT
from app.env import EXEC_PATH
from app.utils.helpers.logger import Log
from app.utils.helpers.network import get_ip_address
from app.utils.helpers.multitask import multithread
from app.gui.web.wsgi import application
from app.gui.web.settings import WEB_PACKAGE


def run_server():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", WEB_PACKAGE + ".settings")
    Log.info("Starting the django web-server in a parallel thread")
    host = get_ip_address()
    if host is None:
        host = APP_WEB_HOST
    app_server = simple_server.make_server(host, APP_WEB_PORT, application)
    # Start the django web-server in a parallel thread
    multithread(app_server.serve_forever, (), True, 1)
    Log.success("Django web-server started!")
    Log.info("Host: " + str(host))
    Log.info("Port: " + str(APP_WEB_PORT))
    webbrowser.open(host + ':' + str(APP_WEB_PORT), new=2)


def django_cmd(args):
    # Go to "web" directory
    if 'runserver' not in args:
        os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'web'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", WEB_PACKAGE + ".settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line([EXEC_PATH + ' --django', ] + args)
