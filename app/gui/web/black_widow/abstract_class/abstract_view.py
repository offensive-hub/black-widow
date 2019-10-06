"""
*********************************************************************************
*                                                                               *
* abstract_view.py -- Abstract view of black-widow.                             *
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

from django.views.generic import TemplateView

from app.utils.helpers.util import is_listable


class AbstractView(TemplateView):
    """
    Abstract view extended by application views
    """
    name = None

    def session_put(self, session, value):
        """
        :type session: django.contrib.sessions.backends.db.SessionStore
        :type value: object
        """
        session[self.name] = value

    def session_get(self, session, params):
        """
        :type session: django.contrib.sessions.backends.db.SessionStore
        :type params: dict
        """
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
                return_params[key] = return_values
            else:
                return_params[key] = {
                    {
                        values: (session_value is not None)
                    }
                }
        return return_params
