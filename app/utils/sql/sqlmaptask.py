"""
*********************************************************************************
*                                                                               *
* sqlmaptask.py -- sqlmap task.                                                 *
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

import requests

from app.utils.helpers.logger import Log
from app.utils.helpers.serializer import JsonSerializer
from app.utils.requests import request


class SqlmapTask:
    """
    The SqlmapTask class
    """

    def __init__(self, task_id: str, base_url: str):
        self.id = task_id
        self.base_url = base_url

    # Public static methods

    @staticmethod
    def task_new(base_url: str):
        """
        Create a new task
        :param base_url: The base_url of sqlmap-api (eg. "http://127.0.0.1:8775")
        :rtype: SqlmapTask
        """
        r_data = SqlmapTask.request(base_url + '/task/new')
        return SqlmapTask(r_data['taskid'], base_url)

    @staticmethod
    def task_list(base_url: str):
        """
        Pull task list
        :param base_url: The base_url of sqlmap-api (eg. "http://127.0.0.1:8775")
        :rtype: dict
        """
        r_data = SqlmapTask.request(base_url + '/admin/list')
        tasks = dict()
        for task_id, task in r_data['tasks'].items():
            tasks[task_id] = SqlmapTask(task_id, base_url)
        return tasks

    @staticmethod
    def task_flush(base_url: str):
        """
        Flush task spool (delete all tasks)
        :param base_url: The base_url of sqlmap-api (eg. "http://127.0.0.1:8775")
        """
        SqlmapTask.request(base_url + '/admin/flush')

    @staticmethod
    def request(url: str) -> dict:
        """
        Send a request to sqlmap-api server and then load the data json as dict
        :param url: The url (eg. "http://127.0.0.1:8775/task/new")
        :rtype: dict
        """
        response = request(url)
        r_data = JsonSerializer.load_json(response.text)
        print(r_data)
        if not r_data['success']:
            Log.error('Response of ' + url + ' has { success = False }')
            raise requests.RequestException('Request to ' + url + ' failed')
        return r_data

    # Public methods

    def task_delete(self):
        """
        Delete this existing task
        """
        self._task_request('delete')

    def scan_kill(self):
        """
        Kill the scan
        """
        self._scan_request('kill')

    def scan_status(self):
        """
        Returns status of the scan
        """
        self._scan_request('status')

    def scan_data(self):
        """
        Retrieve the data of the scan
        """
        self._scan_request('data')

    # Private methods

    def _request(self, path: str):
        url = self.base_url + path
        return SqlmapTask.request(url)

    def _task_request(self, action):
        return self._request('/task/' + self.id + '/' + action)

    def _scan_request(self, action):
        return self._request('/scan/' + self.id + '/' + action)
