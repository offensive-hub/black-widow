"""
*********************************************************************************
*                                                                               *
* sniffing_view.py -- Django Sniffing views.                                    *
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
from time import sleep

from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.env import APP_STORAGE_OUT
from app.manager.sniffer import PcapSniffer
from app.service import JsonSerializer, MultiTask, Log
from app.helper import network, util

from .abstract_sniffing_view import AbstractSniffingView


class Sniffing:
    """
    Sniffing Container View
    """
    class SettingsView(AbstractSniffingView):
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
            sniffing_jobs = self._get_sniffing_jobs(request.session)
            view_params = self.session_get(request.session, {
                'interfaces': network.get_interfaces()
            })
            view_params.update({
                'jobs': sniffing_jobs
            })
            return render(request, self.template_name, view_params)

        def post(self, request):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponseRedirect
            """
            sniffing_jobs = self._get_sniffing_jobs(request.session)

            job_id = len(sniffing_jobs)

            session_job_params: dict = request.POST.dict()
            if session_job_params.get('interfaces') is not None:
                session_job_params['interfaces'] = request.POST.getlist('interfaces')

            pcap_file = request.FILES.get('pcap')
            if pcap_file is not None:
                session_job_params['pcap'] = self.upload_file(pcap_file)
            else:
                session_job_params['pcap'] = None

            out_json_file = os.path.join(self.storage_out_dir, util.now() + '_SNIFFING_' + str(job_id) + '.json')

            session_job_params.update({
                'id': job_id,
                'out_json_file': out_json_file,
                'status': signal.SIGCONT.name
            })

            def callback(pkt: dict):
                """
                :type pkt: dict
                """
                JsonSerializer.add_item_to_dict(pkt['number'], pkt, out_json_file)

            def target():
                """
                The target function used by parallel process
                """
                PcapSniffer.sniff(
                    filters=session_job_params.get('filters'),
                    src_file=session_job_params.get('pcap'),
                    interfaces=session_job_params.get('interfaces'),
                    limit_length=10000,
                    callback=callback
                )

            session_job_params['pidfile'] = MultiTask.multiprocess(target, asynchronous=True, cpu=1)
            session_job_params.pop('csrfmiddlewaretoken', None)
            sniffing_jobs[job_id] = session_job_params

            self._set_sniffing_jobs(request.session, sniffing_jobs)

            return redirect('sniffing/capture?job_id=' + str(job_id))

    class CaptureView(AbstractSniffingView):
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
            Log.info("Showing job #" + str(job_id))
            return render(request, self.template_name)

        def post(self, request):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            sniffing_jobs = self._get_sniffing_jobs(request.session)
            request_params: dict = request.POST.dict()
            job_id = request_params.get('job_id')
            if type(sniffing_jobs) is dict:
                sniffing_job = sniffing_jobs.get(job_id)
            else:
                sniffing_job = None

            if sniffing_job is None:
                return JsonResponse({
                    'message': 'Unable to find the requested job'
                }, status=400)

            out_json_file = sniffing_job.get('out_json_file')

            signal_job = request_params.get('signal')
            if signal_job is not None:
                signal_job = int(signal_job)
                Log.info("Sending signal " + str(signal_job) + " to job #" + str(job_id))

                pid = AbstractSniffingView._get_job_pid(sniffing_jobs[job_id])

                if pid is None:
                    Log.error("The process " + str(pid) + " does not exists")
                else:
                    job = sniffing_jobs[job_id]
                    try:
                        os.kill(int(pid), signal_job)
                        Log.info("Signal " + str(signal_job) + " sent to job #" + str(job_id))
                        job['status'] = signal.Signals(signal_job).name
                    except ProcessLookupError:
                        Log.error("The process " + str(pid) + " does not exists")
                    if signal_job == signal.SIGABRT:    # 6 = Abort permanently by cleaning job
                        AbstractSniffingView._clean_job(job)
                        sniffing_jobs.pop(job_id, None)

                    self._set_sniffing_jobs(request.session, sniffing_jobs)

                return JsonResponse({
                    'job_id': request_params.get('job_id'),
                    'signal': signal_job,
                    'message': 'Signal sent'
                }, status=200)

            page = request_params.get('page')
            page_size = request_params.get('page_size')

            out_json_dict = JsonSerializer.get_dictionary(out_json_file)
            attempts = 0
            while len(out_json_dict) == 0:
                sleep(0.2)
                # Prevent parallel access errors to file
                out_json_dict = JsonSerializer.get_dictionary(out_json_file)
                attempts += 1
                if attempts >= 5:
                    break

            out_dict = util.sort_dict(dict(sorted(
                out_json_dict.items(),
                key=lambda e: int(e[1]['number']),
                reverse=True
            )))

            pagination = self.pagination(out_dict, page, page_size)

            job_id = request_params.get('job_id')

            pagination.update({
                'job': {
                    'id': job_id,
                    'status': sniffing_jobs[job_id]['status']
                }
            })
            return JsonResponse(pagination, status=200)
