"""
WSGI config for web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from app.env import ROOT_PATH, APP_WEB_PACKAGE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", APP_WEB_PACKAGE + ".settings")
os.environ.setdefault("SITE_ROOT", ROOT_PATH)

application = get_wsgi_application()
