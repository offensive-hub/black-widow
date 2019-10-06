"""
*********************************************************************************
*                                                                               *
* views.py -- Django views of black-widow.                                      *
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
from django.views.generic import TemplateView

from app.gui.web.settings import STATICFILES_DIRS
from app.utils.helpers import network
# from .abstract_class import AbstractView

# Create your views here.


def index(request):
    return render(request, 'index.html')


class Sniffing:
    name = 'sniffing'

    class InterfaceView(TemplateView):
        template_name = Sniffing.name + '/interface.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            """
            return render(request, self.template_name, {
                'network_interfaces': network.get_interfaces()
            })

    class FilterView(TemplateView):
        template_name = 'sniffing/filter.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            """
            return render(request, self.template_name)


def user(request):
    return render(request, 'user.html')


def tables(request):
    return render(request, 'tables.html')


def typography(request):
    return render(request, 'typography.html')


def icons(request):
    return render(request, 'icons.html')


def notifications(request):
    """
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: django.http.HttpResponse
    """
    return render(request, 'notifications.html')


def upgrade(request):
    """
    :param request:
    :return: django.http.HttpResponse
    """
    return render(request, 'upgrade.html')


def static(request, path):
    """
    Manage requested static file (for non-DEBUG mode compatibility without web-server)
    :type path: str
    :type request: django.core.handlers.wsgi.WSGIRequest
    """
    for directory in STATICFILES_DIRS:
        static_file = os.path.join(directory, path)
        if os.path.isfile(static_file):
            return FileResponse(open(static_file, 'rb'), as_attachment=False)
    return HttpResponseNotFound()
