"""
WSGI config for web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from app.gui.web.settings import WEB_PACKAGE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", WEB_PACKAGE + ".settings")

application = get_wsgi_application()
