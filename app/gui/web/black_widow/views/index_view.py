"""
*********************************************************************************
*                                                                               *
* index_view.py -- Django index and static views.                               *
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

from django.http import HttpResponseNotFound, FileResponse
from django.shortcuts import render

from black_widow.app.gui.web.settings import STATICFILES_DIRS


def index(request):
    """
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: django.http.HttpResponse
    """
    return render(request, 'index.html')


def user(request):
    """
    :type request: django.core.handlers.wsgi.WSGIRequest
    :rtype: django.http.HttpResponse
    """
    return render(request, 'user.html')


def tables(request):
    """
    :type request: django.core.handlers.wsgi.WSGIRequest
    :rtype: django.http.HttpResponse
    """
    return render(request, 'tables.html')


def typography(request):
    """
    :type request: django.core.handlers.wsgi.WSGIRequest
    :rtype: django.http.HttpResponse
    """
    return render(request, 'typography.html')


def icons(request):
    """
    :type request: django.core.handlers.wsgi.WSGIRequest
    :rtype: django.http.HttpResponse
    """
    return render(request, 'icons.html')


def notifications(request):
    """
    :type request: django.core.handlers.wsgi.WSGIRequest
    :rtype: django.http.HttpResponse
    """
    return render(request, 'notifications.html')


def upgrade(request):
    """
    :type request: django.core.handlers.wsgi.WSGIRequest
    :rtype: django.http.HttpResponse
    """
    return render(request, 'upgrade.html')


# noinspection PyUnusedLocal
def static(request, path):
    """
    Manage requested static file (for non-DEBUG mode compatibility without web-server)
    :type request: django.core.handlers.wsgi.WSGIRequest
    :type path: str
    :rtype: django.http.HttpResponse
    """
    for directory in STATICFILES_DIRS:
        static_file = os.path.join(directory, path)
        if os.path.isfile(static_file):
            return FileResponse(open(static_file, 'rb'))
    return HttpResponseNotFound()
