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

from django.http import HttpResponseNotFound, FileResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile

from app.gui.web.settings import STATICFILES_DIRS
from app.utils.helpers import network
from app.utils.sniffing.pcap import sniff_pcap

from .abstract_class import AbstractView


# Create your views here.


def index(request):
    """
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: django.http.HttpResponse
    """
    return render(request, 'index.html')


class Sniffing:
    """
    Sniffing Container View
    """
    class SettingsView(AbstractView):
        """
        Sniffing View
        """
        name = 'sniffing.settings'
        template_name = 'sniffing/settings.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            view_params = self.session_get(request.session, {
                'interfaces': network.get_interfaces()
            })
            return render(request, self.template_name, view_params)

        def post(self, request):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponseRedirect
            """
            pcap_file: InMemoryUploadedFile = request.FILES.get('pcap')
            if pcap_file is not None:
                uploaded_file = self.upload_file(pcap_file)
                # tmp_file = os.path.join(settings.MEDIA_ROOT, path)
                sniff_pcap(
                    filters=request.POST['filters'],
                    src_file=uploaded_file,
                    interface='wlan0',
                    limit_length=10000
                    # callback=TODO: write the callback to send the data to client by using the session
                )
            self.session_put(request.session, request.POST)
            return HttpResponseRedirect(request.path)

    class CaptureView(AbstractView):
        """
        Capture View
        """
        name = 'sniffing.capture'
        template_name = 'sniffing/capture.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            return HttpResponseNotFound()


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
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: django.http.HttpResponse
    """
    return render(request, 'upgrade.html')


# noinspection PyUnusedLocal
def static(request, path):
    """
    Manage requested static file (for non-DEBUG mode compatibility without web-server)
    :type request: django.core.handlers.wsgi.WSGIRequest
    :type path: str
    """
    for directory in STATICFILES_DIRS:
        static_file = os.path.join(directory, path)
        if os.path.isfile(static_file):
            return FileResponse(open(static_file, 'rb'), as_attachment=False)
    return HttpResponseNotFound()
