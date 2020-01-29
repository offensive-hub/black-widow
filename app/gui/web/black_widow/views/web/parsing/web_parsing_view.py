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

from django.shortcuts import render

from black_widow.app.gui.web.black_widow.models import WebParsingJobModel
from black_widow.app.gui.web.black_widow.views.abstract_view import AbstractView


class WebParsing:
    """
    Web Parsing Container View
    """
    class SettingsView(AbstractView):
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
                'jobs': WebParsingJobModel.all()
            }
            return render(request, self.template_name, view_params)

    class ParseView(AbstractView):
        """
        Web Parsing Parse View
        """
        name = 'web parsing'
        template_name = 'web/parsing/parse.html'
