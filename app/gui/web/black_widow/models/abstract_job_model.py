"""
*********************************************************************************
*                                                                               *
* abstract_job_model.py -- A sniffing job info.                                 *
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

from datetime import datetime
from time import sleep

from django.db import models
from django.utils.timezone import now

from black_widow.app.gui.web.black_widow.models.abstract_model import AbstractModel
from black_widow.app.helpers import storage
from black_widow.app.helpers.util import pid_exists, sort_dict, reverse_dict
from black_widow.app.services import MultiTask, Log, JsonSerializer


class AbstractJobModel(AbstractModel):
    """
    Django Abstract Job Model
    """
    json_file: str = models.CharField(max_length=250, null=False)
    status: int = models.PositiveIntegerField(null=False, default=signal.SIGCONT)
    pid: int = models.PositiveIntegerField(null=False)
    _pid_file: str = models.CharField(max_length=250, null=False)
    created_at: datetime = models.DateTimeField(default=now, editable=False)
    json_sort_value: str = None

    class Meta:
        abstract = True

    @staticmethod
    def _all(model_class) -> models.query.QuerySet:
        """
        :param model_class: A class that implements AbstractJobModel
        :return: All existent jobs of model_class
        """
        jobs = model_class.objects.all().order_by('-id')
        for job in jobs:
            job: AbstractJobModel
            job.self_check()
        return jobs

    def self_check(self):
        if self.status not in (signal.SIGKILL, signal.SIGABRT) and not pid_exists(self.pid):
            self.status = signal.SIGKILL
            self.save()

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
        if self.status == sig:
            return
        Log.info("Sending signal " + str(sig) + " to job #" + str(self.id) + ' (' + str(self.pid) + ')')
        self.status = sig
        try:
            os.kill(self.pid, sig)
        except ProcessLookupError:
            # Process does not exists
            pass
        self.save()
        Log.success("Signal " + str(sig) + " sent to job #" + str(self.id) + ' (' + str(self.pid) + ')')

    def delete(self, using=None, keep_parents=False):
        self.kill(signal.SIGKILL)
        if not storage.delete(self.json_file):
            return False
        if not storage.delete(self.pid_file):
            return False
        return super(AbstractJobModel, self).delete(using, keep_parents)

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
        if self.json_sort_value is None:
            return reverse_dict(json_dict)
        return sort_dict(dict(sorted(
            json_dict.items(),
            key=lambda e: int(e[1][self.json_sort_value]),
            reverse=True
        )))

    @property
    def total(self) -> int:
        json_sort_value = self.json_sort_value
        self.json_sort_value = None
        total = len(self.json_dict)
        self.json_sort_value = json_sort_value
        return total
