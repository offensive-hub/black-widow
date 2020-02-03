"""
*********************************************************************************
*                                                                               *
* abstract_job_view.py -- Django Abstract Job view                              *
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

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, render

from black_widow.app.gui.web.black_widow.models.abstract_job_model import AbstractJobModel
from black_widow.app.gui.web.black_widow.views.abstract_view import AbstractView
from black_widow.app.services import Log


class AbstractJobView(AbstractView):
    model_class: AbstractJobModel = None

    """
    Abstract Job View
    """
    def _get_job(self, request, redirect_url: str):
        """
        Show the requested job
        :type request: django.core.handlers.wsgi.WSGIRequest
        :param redirect_url: The url to redirect the request in case of errors
        :return: django.http.HttpResponse
        """
        request_params: dict = request.GET.dict()

        try:
            job_id = int(request_params.get('id'))
        except (ValueError, TypeError) as e:
            Log.error(str(e))
            return redirect(redirect_url)

        Log.info("Showing job #" + str(job_id))

        try:
            job = self.model_class.objects.get(id=job_id)
        except ObjectDoesNotExist:
            return redirect(redirect_url)

        return render(request, self.template_name, {
            'job': job
        })

    def _post_job(self, request) -> JsonResponse:
        """
        :type request: django.core.handlers.wsgi.WSGIRequest
        :return: django.http.JsonResponse
        """
        # noinspection PyTypeChecker
        job: AbstractJobModel = None
        request_params: dict = request.POST.dict()
        job_id = request_params.get('id')
        try:
            job_id = int(job_id)
            job = self.model_class.objects.get(id=job_id)
        except ValueError:
            pass
        except Exception as e:
            Log.error(str(e))

        if job is None:
            return JsonResponse({
                'message': 'Unable to find the requested job'
            }, status=400)

        signal_job = request_params.get('signal')
        if signal_job is not None:
            signal_job = int(signal_job)

            if signal_job == 0:   # Custom signal 0 = Restart capturing
                job_new = self._copy_job(job)
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
                    }, status=400)

            return JsonResponse({
                'id': job_id,
                'signal': signal_job,
                'message': 'Signal sent'
            }, status=200)

        job.self_check()

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

    def _copy_job(self, job: AbstractJobModel) -> AbstractJobModel:
        raise NotImplementedError("Abstract method _copy_job")
