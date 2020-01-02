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

from django.db import models

from app.gui.web.black_widow.models.abstract_model import AbstractModel
from app.helper import storage
from app.service import MultiTask


class SniffingJobModel(AbstractModel):
    status: int = models.PositiveIntegerField(null=False, default=signal.SIGCONT)
    filters: str = models.CharField(max_length=500, null=True)
    _interfaces: str or None = models.TextField(null=True)
    json_file: str = models.CharField(max_length=250, null=False)
    pcap_file: str = models.CharField(max_length=250, null=True)
    pid: int = models.PositiveIntegerField(null=False)
    _pid_file: str = models.CharField(max_length=250, null=False)

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

    def kill(self, sig: int):
        """
        Send a signal to process which is running this job
        :param sig: The signal as integer (eg. 9 for SIGKILL)
        """
        self.status = sig
        os.kill(self.pid, sig)

    def get_dict(self) -> dict:
        """
        Get this model as dictionary
        :return:
        """
        return {
            'id': self.id,
            'filters': self.filters,
            'interfaces': self.interfaces,
            'json_file': self.json_file,
            'pcap_file': self.pcap_file,
            'pid': self.pid,
            'pid_file': self.pid_file,
            'status': self.status_name
        }

    def delete(self, using=None, keep_parents=False):
        if self.status not in (signal.SIGKILL, signal.SIGABRT):
            self.kill(signal.SIGKILL)
        storage.delete(self.json_file)
        return super(SniffingJobModel, self).delete(using, keep_parents)

    def __str__(self) -> str:
        return str(self.get_dict())
