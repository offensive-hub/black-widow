"""
*********************************************************************************
*                                                                               *
* web_parsing_view.py -- Django Web Parsing view.                               *
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
from django.http import JsonResponse
from django.shortcuts import render, redirect

from black_widow.app.gui.web.black_widow.models import WebParsingJobModel
from black_widow.app.gui.web.black_widow.views.web.parsing.abstract_web_parsing_view import AbstractWebParsingView


class WebParsing:
    """
    Web Parsing Container View
    """
    class SettingsView(AbstractWebParsingView):
        """
        Web Parsing Settings View
        """
        name = 'web parsing'
        template_name = 'web/parsing/settings.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            view_params = {
                'types': WebParsingJobModel.TYPES,
                'tags': WebParsingJobModel.PARSE_TAGS,
                'jobs': WebParsingJobModel.all()
            }
            return render(request, self.template_name, view_params)

        def post(self, request):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponseRedirect
            """
            request_params: dict = request.POST.dict()
            job = self._new_job(
                request_params.get('url'),
                request_params.get('type'),
                request_params.get('depth'),
                request_params.get('tags'),
                request_params.get('cookies')
            )
            return redirect('/web/parsing/parse?id=' + str(job.id))

    class ParseView(AbstractWebParsingView):
        """
        Web Parsing Parse View
        """
        name = 'web parsing'
        template_name = 'web/parsing/parse.html'

        def get(self, request, *args, **kwargs):
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.HttpResponse
            """
            return self._get_job(request, redirect_url='/web/parsing')

        def post(self, request) -> JsonResponse:
            """
            :type request: django.core.handlers.wsgi.WSGIRequest
            :return: django.http.JsonResponse
            """
            return self._post_job(request)
