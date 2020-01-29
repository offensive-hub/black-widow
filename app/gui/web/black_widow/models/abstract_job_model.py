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

from django.db import models
from django.utils.timezone import now

from black_widow.app.gui.web.black_widow.models.abstract_model import AbstractModel
from black_widow.app.helpers.util import pid_exists
from black_widow.app.services import MultiTask, Log


class AbstractJobModel(AbstractModel):
    """
    Django Abstract Job Model
    """
    status: int = models.PositiveIntegerField(null=False, default=signal.SIGCONT)
    pid: int = models.PositiveIntegerField(null=False)
    _pid_file: str = models.CharField(max_length=250, null=False)
    created_at: str = models.DateTimeField(default=now, editable=False)

    @staticmethod
    def _all(model_class) -> models.query.QuerySet:
        """
        :param model_class: A class that implements AbstractJobModel
        :return: All existent jobs of model_class
        """
        jobs = model_class.objects.all().order_by('-id')
        for job in jobs:
            job: AbstractJobModel
            if job.status not in (signal.SIGKILL, signal.SIGABRT):
                if not pid_exists(job.pid):
                    job.status = signal.SIGKILL
                    job.save()
        return jobs

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
        os.kill(self.pid, sig)
        self.save()
        Log.success("Signal " + str(sig) + " sent to job #" + str(self.id) + ' (' + str(self.pid) + ')')
