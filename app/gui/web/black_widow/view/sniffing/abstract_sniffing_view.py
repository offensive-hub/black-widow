"""
*********************************************************************************
*                                                                               *
* abstract_sniffing_view.py -- Django Abstract Sniffing view.                   *
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

from app.env import APP_STORAGE_OUT
from app.service import MultiTask
from app.helper import storage
from app.helper.util import pid_exists

from app.gui.web.black_widow.view.abstract_view import AbstractView


class AbstractSniffingView(AbstractView):
    """
    Abstract Sniffing View
    """

    storage_out_dir = os.path.join(APP_STORAGE_OUT, 'sniffing')
    storage.check_folder(storage_out_dir)
    if not os.access(storage_out_dir, os.X_OK):
        os.chmod(storage_out_dir, 0o0755)

    @staticmethod
    def _get_job_pid(job: dict) -> int or None:
        """
        :type job: dict
        :rtype: int or None
        """
        pids = MultiTask.get_pids_from_file(job.get('pidfile'))
        if len(pids) >= 1:
            try:
                return int(pids[0])
            except ValueError:
                pass
        return None

    @staticmethod
    def _clean_job(job: dict):
        """
        :type job: dict
        """
        pid = AbstractSniffingView._get_job_pid(job)
        if pid is not None:
            try:
                os.kill(int(pid), signal.SIGKILL)
            except ProcessLookupError:
                pass
        storage.delete(job['out_json_file'])
        storage.delete(job['pidfile'])

    def _get_sniffing_jobs(self, session) -> dict:
        """
        :type session: django.contrib.sessions.backends.db.SessionStore
        :rtype: dict
        """
        session_params = self.session_get(session)
        sniffing_jobs = session_params.get('sniffing_jobs')
        update_session = False
        if type(sniffing_jobs) is not dict:
            sniffing_jobs = dict()
        storage_files = storage.ls(self.storage_out_dir)
        job_files = []
        job_ids = list(sniffing_jobs.keys())
        for job_id in job_ids:
            job = sniffing_jobs[job_id]
            pid = AbstractSniffingView._get_job_pid(job)
            job_file = job.get('out_json_file')
            if not pid_exists(pid):
                if job_file in storage_files:
                    job['status'] = signal.SIGKILL.name
                    job_files.append(job_file)
                else:
                    AbstractSniffingView._clean_job(job)
                    sniffing_jobs.pop(job_id, None)
                    update_session = True
            else:
                job_files.append(job_file)
        for storage_file in storage_files:
            if storage_file not in job_files:
                job_id = len(sniffing_jobs)
                job = {
                    'id': job_id,
                    'out_json_file': storage_file,
                    'status': signal.SIGKILL.name,
                    'pcap': storage_file,
                    'interfaces': None
                }
                sniffing_jobs[job_id] = job
                update_session = True
        if update_session:
            self._set_sniffing_jobs(session, sniffing_jobs)
        return sniffing_jobs

    def _set_sniffing_jobs(self, session, sniffing_jobs):
        """
        :type session: django.contrib.sessions.backends.db.SessionStore
        :type sniffing_jobs: dict
        """
        session_params = self.session_get(session)
        session_params['sniffing_jobs'] = sniffing_jobs
        self.session_update(session, session_params)
