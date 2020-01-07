"""
*********************************************************************************
*                                                                               *
* sniffing_job_model.py -- A sniffing job info.                                 *
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

from time import sleep
from django.db import models
from django.utils.timezone import now

from black_widow.app.gui.web.black_widow.models.abstract_model import AbstractModel
from black_widow.app.helpers import storage
from black_widow.app.helpers.util import sort_dict, pid_exists
from black_widow.app.services import MultiTask, JsonSerializer, Log


class SniffingJobModel(AbstractModel):
    status: int = models.PositiveIntegerField(null=False, default=signal.SIGCONT)
    filters: str = models.TextField(null=True)
    _interfaces: str or None = models.TextField(null=False)
    json_file: str = models.CharField(max_length=250, null=False)
    pcap_file: str = models.CharField(max_length=250, null=True)
    pid: int = models.PositiveIntegerField(null=False)
    _pid_file: str = models.CharField(max_length=250, null=False)
    created_at: str = models.DateTimeField(default=now, editable=False)

    @staticmethod
    def all() -> models.query.QuerySet:
        sniffing_jobs = SniffingJobModel.objects.all().order_by('-id')
        for sniffing_job in sniffing_jobs:
            sniffing_job: SniffingJobModel
            if sniffing_job.status not in (signal.SIGKILL, signal.SIGABRT):
                if not pid_exists(sniffing_job.pid):
                    sniffing_job.status = signal.SIGKILL
                    sniffing_job.save()
        return sniffing_jobs

    @property
    def interfaces(self) -> list or None:
        if self._interfaces is None:
            return None
        return self._interfaces.split(';')

    @interfaces.setter
    def interfaces(self, value: list or None):
        if value is None:
            self._interfaces = None
        else:
            self._interfaces = ';'.join(value)

    @property
    def pid_file(self) -> str:
        return self._pid_file

    @pid_file.setter
    def pid_file(self, value: str):
        self._pid_file = value
        pids = MultiTask.get_pids_from_file(self.pid_file)
        if len(pids) != 1:
            raise ChildProcessError("Unable to find process PID of this Sniffing Job")
        self.pid = int(pids[0])

    @property
    def status_name(self) -> str:
        return signal.Signals(self.status).name

    @property
    def json_dict(self) -> dict:
        attempts = 0
        json_dict = JsonSerializer.get_dictionary(self.json_file)
        while len(json_dict) == 0:
            sleep(0.2)
            # Prevents parallel access errors to file
            json_dict = JsonSerializer.get_dictionary(self.json_file)
            attempts += 1
            if attempts >= 5:
                break
        return sort_dict(dict(sorted(
            json_dict.items(),
            key=lambda e: int(e[1]['number']),
            reverse=True
        )))

    def kill(self, sig: int):
        """
        Send a signal to process which is running this job
        :param sig: The signal as integer (eg. 9 for SIGKILL)
        """
        Log.info("Sending signal " + str(sig) + " to job #" + str(self.id) + ' (' + str(self.pid) + ')')
        self.status = sig
        os.kill(self.pid, sig)
        self.save()
        Log.success("Signal " + str(sig) + " sent to job #" + str(self.id) + ' (' + str(self.pid) + ')')

    def delete(self, using=None, keep_parents=False):
        if self.status not in (signal.SIGKILL, signal.SIGABRT):
            self.kill(signal.SIGKILL)
        if not storage.delete(self.json_file):
            return False
        if not storage.delete(self.pid_file):
            return False
        return super(SniffingJobModel, self).delete(using, keep_parents)

    def __str__(self) -> str:
        return 'SniffingJobModel(' + str({
            'id': self.id,
            'filters': self.filters,
            'interfaces': self.interfaces,
            'json_file': self.json_file,
            'pcap_file': self.pcap_file,
            'pid': self.pid,
            'pid_file': self.pid_file,
            'status': self.status_name
        }) + ')'
