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

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from black_widow.app.gui.web.black_widow.views.abstract_view import AbstractView
from black_widow.app.services import Log


class AbstractJobView(AbstractView):
    model_class = None

    """
    Abstract Job View
    """
    def _get_job(self, request, redirect_url: str):
        """
        Show the requested job
        :type request: django.core.handlers.wsgi.WSGIRequest
        :param redirect_url:
        :return:
        """
        request_params: dict = request.GET.dict()

        try:
            job_id = int(request_params.get('id'))
        except (ValueError, TypeError):
            return redirect(redirect_url)

        Log.info("Showing job #" + str(job_id))

        try:
            sniffing_job = self.model_class.objects.get(id=job_id)
        except ObjectDoesNotExist:
            return redirect(redirect_url)

        return render(request, self.template_name, {
            'job': sniffing_job
        })
