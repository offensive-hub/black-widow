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
import signal

from django.http import HttpResponseNotFound, FileResponse
from django.shortcuts import render, redirect

from jsonview.decorators import json_view

from app.env import APP_STORAGE_OUT
from app.gui.web.settings import STATICFILES_DIRS
from app.utils.helpers import network
from app.utils.sniffing.pcap import sniff_pcap
from app.utils.helpers import util
from app.utils.helpers import storage
from app.utils.helpers.multitask import multiprocess

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
        name = 'sniffing'
        template_name = 'sniffing/settings.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            # TODO: show current capturing process jobs
            view_params = self.session_get(request.session, {
                'interfaces': network.get_interfaces()
            })
            return render(request, self.template_name, view_params)

        def post(self, request):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponseRedirect
            """
            session_params = self.session_get(request.session)
            sniffing_jobs = session_params.get('sniffing_jobs')
            if sniffing_jobs is None:
                sniffing_jobs = dict()
                job_id = 0
            else:
                job_id = len(sniffing_jobs)

            session_job_params: dict = request.POST.dict()

            pcap_file = request.FILES.get('pcap')
            if pcap_file is not None:
                session_job_params['pcap'] = self.upload_file(pcap_file)
            else:
                session_job_params['pcap'] = None

            out_json_file = APP_STORAGE_OUT + '/' + util.now() + '_SNIFFING_' + str(job_id) + '.json'
            job_killed_file = out_json_file + '.KILL'

            session_job_params.update({
                'id': job_id,
                'out_json_file': out_json_file
            })

            def callback(pkt: dict):
                """
                :type pkt: dict
                """
                if os.path.exists(job_killed_file):
                    storage.delete(job_killed_file)
                    util.Log.success("Sniffing Job #" + str(job_id) + " killed")
                    os.kill(os.getpid(), signal.SIGKILL)
                    return

                util.add_json_item(pkt['number'], pkt, out_json_file)

            def target():
                """
                The target function used by parallel process
                """
                sniff_pcap(
                    filters=session_job_params.get('filters'),
                    src_file=session_job_params.get('pcap'),
                    interface=session_job_params.get('interfaces'),
                    limit_length=10000,
                    callback=callback  # TODO: write the callback to send the data to client by using the session
                )

            multiprocess(target, asynchronous=True, cpu=1)

            session_job_params.pop('csrfmiddlewaretoken', None)
            sniffing_jobs[job_id] = session_job_params
            session_params['sniffing_jobs'] = sniffing_jobs

            self.session_update(request.session, session_params)

            return redirect('sniffing/capture?job_id=' + str(job_id))

    class CaptureView(AbstractView):
        """
        Capture View
        """
        name = 'sniffing'
        template_name = 'sniffing/capture.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            request_params: dict = request.GET.dict()
            job_id = request_params.get('job_id')
            util.Log.info("Showing job #" + str(job_id))
            return render(request, self.template_name)

        @json_view
        def post(self, request):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            session_params = self.session_get(request.session)
            sniffing_jobs = session_params.get('sniffing_jobs')
            request_params: dict = request.POST.dict()
            job_id = request_params.get('job_id')
            if type(sniffing_jobs) is dict:
                sniffing_job = sniffing_jobs.get(job_id)
            else:
                sniffing_job = None

            if sniffing_job is None:
                return {
                    'message': 'Unable to find the requested job'
                }, 400

            out_json_file = sniffing_job.get('out_json_file')

            kill_job = request_params.get('kill')
            if kill_job is not None and int(kill_job) == 1:
                kill_job_file = out_json_file + '.KILL'
                open(kill_job_file, 'a').close()
                sniffing_jobs.pop(job_id, None)
                session_params['sniffing_jobs'] = sniffing_jobs
                self.session_update(request.session, session_params)
                return {
                    'job_id': request_params.get('job_id'),
                    'message': 'Job killed'
                }

            out_dict = util.get_json(out_json_file)
            page = request_params.get('page')
            page_size = request_params.get('page_size')
            pagination = AbstractView.pagination(out_dict, page, page_size)

            pagination.update({
                'job_id': request_params.get('job_id')
            })

            return pagination


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
