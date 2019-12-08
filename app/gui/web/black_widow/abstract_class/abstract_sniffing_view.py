"""
*********************************************************************************
*                                                                               *
* abstract_sniffing_view.py -- Abstract sniffing view                           *
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

from app.gui.web.black_widow.abstract_class import AbstractView


class AbstractSniffingView(AbstractView):
    """
    Abstract Sniffing View
    """
    def _get_sniffing_jobs(self, session) -> dict:
        """
        :type session: django.contrib.sessions.backends.db.SessionStore
        :rtype: dict
        """
        session_params = self.session_get(session)
        sniffing_jobs = session_params.get('sniffing_jobs')
        if type(sniffing_jobs) is not dict:
            sniffing_jobs = dict()
        return sniffing_jobs

    def _set_sniffing_jobs(self, session, sniffing_jobs):
        """
        :type session: django.contrib.sessions.backends.db.SessionStore
        :type sniffing_jobs: dict
        """
        session_params = self.session_get(session)
        session_params['sniffing_jobs'] = sniffing_jobs
        self.session_update(session, session_params)
