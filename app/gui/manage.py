import os
import webbrowser

from django.core.servers.basehttp import simple_server

from app.env import APP_WEB_PACKAGE, APP_WEB_HOST, APP_WEB_PORT, EXEC_PATH
from app.utils.helpers.logger import Log
from app.gui.web.wsgi import application
from app.utils.helpers.multitask import multithread


def run_server():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", APP_WEB_PACKAGE + ".settings")
    Log.info("Starting the django web-server in a parallel thread")
    app_server = simple_server.make_server(APP_WEB_HOST, APP_WEB_PORT, application)
    # Start the django web-server in a parallel thread
    multithread(app_server.serve_forever, (), True, 1)
    Log.success("Django web-server started!")
    webbrowser.open(APP_WEB_HOST + ':' + str(APP_WEB_PORT), new=2)


def django_cmd(arg):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", APP_WEB_PACKAGE + ".settings")
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
    execute_from_command_line([EXEC_PATH + ' --django', arg])