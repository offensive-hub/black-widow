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

from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.gui.web.black_widow.models import SniffingJobModel
from app.manager.sniffer import PcapSniffer
from app.service import JsonSerializer, Log, MultiTask
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
            request_params: dict = request.POST.dict()
            if request_params.get('interfaces') is not None:
                request_params['interfaces'] = request.POST.getlist('interfaces')
            pcap_file = request.FILES.get('pcap')
            if pcap_file is not None:
                request_params['pcap'] = self.upload_file(pcap_file)
            else:
                request_params['pcap'] = None

            json_file = os.path.join(self.storage_out_dir, util.now() + '_SNIFFING_.json')

            sniffing_job = SniffingJobModel()
            sniffing_job.filters = request_params.get('filters')
            sniffing_job.pcap_file = request_params.get('pcap')
            sniffing_job.interfaces = request_params.get('interfaces')
            sniffing_job.json_file = json_file

            def _sniffer_callback(pkt: dict):
                """
                The callback function of packet sniffer.
                This method writes the sniffed packets in a json file
                :param pkt: The sniffed packet
                """
                JsonSerializer.add_item_to_dict(pkt['number'], pkt, sniffing_job.json_file)

            def _sniffer_target():
                """
                Starts the packet sniffing
                """
                PcapSniffer.sniff(
                    filters=sniffing_job.filters,
                    src_file=sniffing_job.pcap_file,
                    interfaces=sniffing_job.interfaces,
                    limit_length=10000,
                    callback=_sniffer_callback
                )

            sniffing_job.pid_file = MultiTask.multiprocess(_sniffer_target, asynchronous=True, cpu=1)
            sniffing_job.save()

            return redirect('sniffing/capture?id=' + str(sniffing_job.id))

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
            if not util.is_root():
                return render(request, self.error_templates.get('root_required'))
            request_params: dict = request.GET.dict()
            try:
                sniffing_job_id = int(request_params.get('id'))
            except ValueError:
                return redirect('sniffing')
            Log.info("Showing job #" + str(sniffing_job_id))
            sniffing_job = SniffingJobModel.objects.get(id=sniffing_job_id)
            if sniffing_job is None:
                return redirect('sniffing')
            return render(request, self.template_name)

        def post(self, request):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            # noinspection PyTypeChecker
            sniffing_job: SniffingJobModel = None
            request_params: dict = request.POST.dict()
            sniffing_job_id = request_params.get('id')
            try:
                sniffing_job_id = int(sniffing_job_id)
                sniffing_job = SniffingJobModel.objects.get(id=sniffing_job_id)
            except ValueError:
                pass

            if sniffing_job is None:
                return JsonResponse({
                    'message': 'Unable to find the requested job'
                }, status=400)

            signal_job = request_params.get('signal')
            if signal_job is not None:
                signal_job = int(signal_job)
                try:
                    sniffing_job.kill(signal_job)
                except ProcessLookupError:
                    Log.warning("The process " + str(sniffing_job.pid) + " does not exists")
                if signal_job == signal.SIGABRT:    # 6 = Abort permanently by cleaning job
                    sniffing_job.delete()
                return JsonResponse({
                    'id': sniffing_job_id,
                    'signal': signal_job,
                    'message': 'Signal sent'
                }, status=200)

            page = request_params.get('page')
            page_size = request_params.get('page_size')
            pagination = self.pagination(sniffing_job.json_dict, page, page_size)
            pagination.update({
                'job': {
                    'id': sniffing_job_id,
                    'status': sniffing_job.status_name
                }
            })

            return JsonResponse(pagination, status=200)
