"""
*********************************************************************************
*                                                                               *
* abstract_view.py -- Django Abstract view.                                     *
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

import itertools
import math

from os.path import join
from django.views.generic import TemplateView

from black_widow.app.helpers.util import is_listable, timestamp
from black_widow.app.helpers import storage
from black_widow.app.env import APP_TMP


class AbstractView(TemplateView):
    """
    Abstract view extended by application views
    """
    name = None
    error_templates = {
        'root_required': 'error/root_required.html'
    }

    def upload_file(self, tmp_file) -> str:
        """
        :param tmp_file: the in-memory uploaded file
        :type tmp_file: django.core.files.uploadedfile.InMemoryUploadedFile
        :rtype: str
        """
        upload_folder = join(APP_TMP, self.name)
        storage.check_folder(upload_folder)
        uploaded_filename = timestamp() + '_' + tmp_file.name
        uploaded_path = join(upload_folder, uploaded_filename)
        storage.delete(uploaded_path)
        with open(uploaded_path, 'wb+') as destination:
            for chunk in tmp_file.chunks():
                destination.write(chunk)
        return str(uploaded_path)

    def session_put(self, session, value: dict):
        """
        :type session: django.contrib.sessions.backends.db.SessionStore
        :type value: dict
        """
        session[self.name] = value

    def session_update(self, session, value: dict):
        """
        :type session: django.contrib.sessions.backends.db.SessionStore
        :type value: dict
        """
        session_value = session.get(self.name)
        if type(session_value) is not dict:
            session_value = value
        else:
            session_value.update(value)
        session[self.name] = session_value

    def session_get(self, session, params=None):
        """
        :type session: django.contrib.sessions.backends.db.SessionStore
        :type params: dict
        :rtype: dict
        """
        if params is None:
            params = {}
        session_params = session.get(self.name)
        if session_params is None:
            session_params = dict()
        return_params = session_params
        for key, values in params.items():
            session_value = session_params.get(key)
            if is_listable(values):
                return_values = dict()
                for value in values:
                    return_values[value] = (value == session_value)
            else:
                return_values = {
                    {
                        values: (session_value is not None)
                    }
                }
            return_params[key] = return_values
        return return_params

    @staticmethod
    def pagination(elements: dict, page: int, page_size: int):
        try:
            page = int(page)
        except TypeError:
            page = 1
        try:
            page_size = int(page_size)
        except TypeError:
            page_size = 10
        elements_tot = len(elements)
        start = page_size * (page - 1)
        stop = start + page_size
        page_end = math.ceil(elements_tot / page_size)
        result = dict(itertools.islice(elements.items(), start, stop))
        return {
            'result': result,
            'page': page,
            'page_start': 1,
            'page_end': page_end,
            'page_size': page_size,
            'total': elements_tot
        }
