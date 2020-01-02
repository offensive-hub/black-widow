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

from django.db import models


class SniffingJobModel(models.Model):
    id: int = models.PositiveIntegerField(primary_key=True)
    pid: int = models.PositiveIntegerField()
    status: int = models.PositiveIntegerField()
    json_file: str = models.CharField(max_length=250)
    pcap_file: str = models.CharField(max_length=250)
    _interfaces: str = models.TextField()

    @property
    def interfaces(self) -> list or None:
        if self._interfaces is None:
            return None
        return self._interfaces.split(';')

    @interfaces.setter
    def interfaces(self, value: list or None):
        if value is None:
            self._my_date = None
        else:
            self._my_date = ';'.join(value)
