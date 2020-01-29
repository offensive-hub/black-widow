"""
*********************************************************************************
*                                                                               *
* web_parsing_model.py -- A web parsing job info model                          *
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

import signal

from time import sleep
from django.db import models
from django.utils.timezone import now

from black_widow.app.gui.web.black_widow.models.abstract_job_model import AbstractJobModel
from black_widow.app.helpers import storage
from black_widow.app.helpers.util import sort_dict
from black_widow.app.services import JsonSerializer


class WebParsingJobModel(AbstractJobModel):
    """
    Django Web Parsing Job Model
    """
    json_file: str = models.CharField(max_length=250, null=False)


    @staticmethod
    def all() -> models.query.QuerySet:
        return AbstractJobModel._all(SniffingJobModel)

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

    def delete(self, using=None, keep_parents=False):
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
