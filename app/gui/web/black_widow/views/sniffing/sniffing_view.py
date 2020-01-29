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

import signal

from django.http import JsonResponse
from django.shortcuts import render, redirect

from black_widow.app.gui.web.black_widow.models import SniffingJobModel
from black_widow.app.services import Log
from black_widow.app.helpers import network, util

from .abstract_sniffing_view import AbstractSniffingView


class Sniffing:
    """
    Sniffing Container View
    """
    class SettingsView(AbstractSniffingView):
        """
        Sniffing Settings View
        """
        name = 'sniffing'
        template_name = 'sniffing/settings.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            if not util.is_root():
                return render(request, self.error_templates.get('root_required'))
            view_params = {
                'interfaces': network.get_interfaces(),
                'jobs': SniffingJobModel.all()
            }
            return render(request, self.template_name, view_params)

        def post(self, request):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponseRedirect
            """
            if not util.is_root():
                return JsonResponse({
                    'message': 'You are not #root'
                }, status=401)
            request_params: dict = request.POST.dict()
            if request_params.get('interfaces') is not None:
                request_params['interfaces'] = request.POST.getlist('interfaces')
            pcap_file = request.FILES.get('pcap')
            if pcap_file is not None:
                request_params['pcap'] = self.upload_file(pcap_file)
            else:
                request_params['pcap'] = None

            job = self.new_job(
                request_params.get('filters'),
                request_params.get('pcap'),
                request_params.get('interfaces'),
            )

            return redirect('/sniffing/capture?id=' + str(job.id))

    class CaptureView(AbstractSniffingView):
        """
        Sniffing Capture View
        """
        name = 'sniffing'
        template_name = 'sniffing/capture.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            if not util.is_root():
                return render(request, self.error_templates.get('root_required'))

            return self._get_job(request, redirect_url='/sniffing')

        def post(self, request):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            # noinspection PyTypeChecker
            job: SniffingJobModel = None
            request_params: dict = request.POST.dict()
            job_id = request_params.get('id')
            try:
                job_id = int(job_id)
                job = SniffingJobModel.objects.get(id=job_id)
            except ValueError:
                pass
            except Exception as e:
                print(type(e))
                print(str(e))

            if job is None:
                return JsonResponse({
                    'message': 'Unable to find the requested job'
                }, status=400)

            signal_job = request_params.get('signal')
            if signal_job is not None:
                signal_job = int(signal_job)

                if signal_job == 0:   # Custom signal 0 = Restart capturing
                    job_new = self.new_job(
                        job.filters,
                        job.pcap_file,
                        job.interfaces,
                    )
                    job_id = job_new.id
                    signal_job = signal.SIGABRT

                try:
                    job.kill(signal_job)
                except ProcessLookupError:
                    Log.warning("The process " + str(job.pid) + " does not exists")

                if signal_job == signal.SIGABRT:    # 6 = Abort permanently by cleaning job
                    if not job.delete():
                        return JsonResponse({
                            'message': 'Unable to delete the job'
                        })

                return JsonResponse({
                    'id': job_id,
                    'signal': signal_job,
                    'message': 'Signal sent'
                }, status=200)

            page = request_params.get('page')
            page_size = request_params.get('page_size')
            pagination = self.pagination(job.json_dict, page, page_size)
            pagination.update({
                'job': {
                    'id': job_id,
                    'status': job.status_name
                }
            })

            return JsonResponse(pagination, status=200)
