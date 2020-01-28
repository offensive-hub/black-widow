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

from black_widow.app.managers.request import HttpRequest
from black_widow.app.services import Log, JsonSerializer


class SqlmapTask:
    """
    The SqlmapTask class
    """

    def __init__(self, task_id: str, base_url: str):
        self.id = task_id
        self.base_url = base_url

    """ Public static methods """

    ##########################
    # Sqlmap Admin functions #
    ##########################

    @staticmethod
    def task_list(base_url: str):
        """
        Pull task list
        :param base_url: The base_url of sqlmap-api (eg. "http://127.0.0.1:8775")
        :rtype: dict
        """
        r_data = SqlmapTask._request(base_url + '/admin/list')
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
        SqlmapTask._request(base_url + '/admin/flush')

    #############################
    # Task management functions #
    #############################

    @staticmethod
    def task_new(base_url: str):
        """
        Create a new task
        :param base_url: The base_url of sqlmap-api (eg. "http://127.0.0.1:8775")
        :rtype: SqlmapTask
        """
        r_data = SqlmapTask._request(base_url + '/task/new')
        return SqlmapTask(r_data['taskid'], base_url)

    ###############
    # Delete task #
    ###############

    def task_delete(self):
        """
        Delete this existing task
        """
        return self.__task_request('delete')

    ##################################
    # Sqlmap core interact functions #
    ##################################

    def option_list(self) -> dict:
        """
        List options for this task
        """
        return self.__option_request('list')

    def option_get(self, options: list) -> dict:
        """
        Get value of option(s) for this task
        :param options: The options to get (eg. [ "cookie", "headers", "referer", ... ])
        """
        return self.__option_request('get', HttpRequest.Type.POST, options)

    def option_set(self, options: dict) -> dict:
        """
        Get value of option(s) for this task
        :param options: The options to set (eg. { "referer": "https://example.com" ])
        """
        return self.__option_request('set', HttpRequest.Type.POST, options)

    ################
    # Handle scans #
    ################

    def scan_start(self):
        """
        Launch the scan
        """
        return self.__scan_request('start', HttpRequest.Type.POST, {})

    def scan_stop(self):
        """
        Stop the scan
        """
        return self.__scan_request('stop')

    def scan_kill(self) -> dict:
        """
        Kill the scan
        """
        return self.__scan_request('kill')

    def scan_status(self) -> dict:
        """
        Returns status of the scan
        """
        return self.__scan_request('status')

    def scan_data(self) -> dict:
        """
        Retrieve the data of the scan
        """
        return self.__scan_request('data')

    def scan_log(self) -> dict:
        """
        Retrieve the log messages of the scan
        """
        return self.__scan_request('log')

    ###################
    # Utils functions #
    ###################

    @staticmethod
    def _request(url: str, request_type: str = HttpRequest.Type.GET, json: dict or list = None) -> dict:
        """
        Send a request to sqlmap-api server and then load the data json as dict
        :param url: The sqlmap-api url (eg. "http://127.0.0.1:8775/task/new")
        :param request_type: get|post|put|patch|delete
        :param json: The json to send
        :rtype: dict
        """
        response = HttpRequest.request(url, request_type, json=json)
        r_data = JsonSerializer.load_json(response.text)
        Log.info('Response data of ' + url + ': ' + str(r_data))
        success = r_data.get('success')
        if success is None:
            # The response has not the status management
            return r_data
        if not success:
            Log.error('Response data of ' + url + ' has { success: False }')
            raise requests.RequestException('Request to ' + url + ' failed')
        return r_data

    """ Private methods """

    def __request(self, path: str, request_type: str = HttpRequest.Type.GET, json: dict or list = None) -> dict:
        """
        :param path: The path for request (eg. "/task/<id>/start")
        :param request_type: get|post|put|patch|delete
        :param json: The json to send
        :rtype: dict
        """
        url = self.base_url + path
        return SqlmapTask._request(url, request_type, json)

    def __option_request(
            self,
            action: str,
            request_type: str = HttpRequest.Type.GET,
            json: dict or list = None
    ) -> dict:
        """
        :param action: The action of option request (eg. "list")
        :param request_type: get|post|put|patch|delete
        :param json: The json to send
        :rtype: dict
        """
        return self.__request('/option/' + self.id + '/' + action, request_type, json)

    def __task_request(self, action: str, request_type: str = HttpRequest.Type.GET, json: dict or list = None) -> dict:
        """
        :param action: The action of task request (eg. "delete")
        :param request_type: get|post|put|patch|delete
        :param json: The json to send
        :rtype: dict
        """
        return self.__request('/task/' + self.id + '/' + action, request_type, json)

    def __scan_request(self, action: str, request_type: str = HttpRequest.Type.GET, json: dict or list = None) -> dict:
        """
        :param action: The action of scan request (eg. "kill")
        :param request_type: get|post|put|patch|delete
        :param json: The json to send
        :rtype: dict
        """
        return self.__request('/scan/' + self.id + '/' + action, request_type, json)
