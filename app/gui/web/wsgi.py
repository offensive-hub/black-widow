"""
WSGI config for web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
# import sys

# from os.path import dirname
from django.core.wsgi import get_wsgi_application

WEB_PACKAGE = 'app.gui.web'

# root_path = dirname(dirname(dirname(dirname(__file__))))    # to access at "app" package
# sys.path.insert(0, root_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", WEB_PACKAGE + ".settings")

application = get_wsgi_application()
