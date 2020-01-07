"""
*********************************************************************************
*                                                                               *
* sqlmapcli.py -- sqlmap client.                                                *
*                                                                               *
* Class to interface with the sqlmap local server.                              *
*                                                                               *
* sqlmap repository:                                                            *
* https://github.com/sqlmapproject/sqlmap                                       *
*                                                                               *
* sqlmap license:                                                               *
* https://raw.githubusercontent.com/sqlmapproject/sqlmap/master/LICENSE         *
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

from pprint import pprint
from sqlmap.lib.utils.api import server as sqlmap_server
from time import sleep

from black_widow.app.managers.request import HttpRequest
from black_widow.app.services import Log, MultiTask
from black_widow.app.helpers.network import check_socket

from .sqlmaptask import SqlmapTask


class SqlmapClient:
    """
    Sqlmap Client
    """

    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = 8775

    _client = None

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        """
        :param host: The host
        :param port: The port
        """
        self.host = host
        self.port = port
        self.base_url = 'http://' + self.host + ':' + str(port)
        # Start the sqlmap-api server in a parallel thread
        Log.info("Starting sqlmap-api server in a parallel thread")
        MultiTask.multithread(sqlmap_server, (self.host, self.port), True, 1)
        while not check_socket(self.host, self.port):
            # Wait sqlmap-api server
            sleep(0.1)
        Log.success("Sqlmap-api server started!")

    """ Public static methods """

    @staticmethod
    def task_list() -> dict:
        """
        :return: The dictionary of existent tasks
        """
        client = SqlmapClient._get_client()
        return SqlmapTask.task_list(client.base_url)

    @staticmethod
    def task_flush():
        """
        Flush task spool (delete all tasks)
        """
        client = SqlmapClient._get_client()
        return SqlmapTask.task_flush(client.base_url)

    @staticmethod
    def try_inject(
            forms: dict,
            cookies: str = '',
            delay: int = 0,
            random_agent: bool = False
    ) -> dict:
        """
        Try injection with all provided forms
        :param forms: dict A dictionary of { "<url>": [ <parsed_form_1>, <parsed_form_2>, ... ], ... }
        :param cookies: str the request cookies
        :param delay: int The delay on each request
        :param random_agent: True if set a random agent for each sqlmap request
        :rtype: dict
        """
        sqlmap_tasks = dict()
        Log.info('Trying injection with cookies: ' + str(cookies))
        for url, page_forms in forms.items():
            page_forms: list    # The forms in page returned by url
            for page_form in page_forms:
                page_form: dict    # The attributes and inputs of form
                action = page_form.get('action')
                inputs = page_form.get('inputs')
                method = page_form.get('method')
                # Foreach form, will created a new SqlmapTask
                pprint(inputs)
                sqlmap_task = SqlmapClient._task_new()
                sqlmap_task.option_set({
                    'cookie': cookies,
                    'agent': HttpRequest.default_agent(),
                    'referer': url,
                    'delay': delay,
                    'randomAgent': random_agent,
                    'method': method,
                    'url': action
                })
                sqlmap_task.option_get([
                    'referer',
                    'agent',
                    'referer',
                    'delay',
                    'randomAgent',
                    'method',
                    'url'
                ])
                sqlmap_tasks[sqlmap_task.id] = sqlmap_task

        return sqlmap_tasks

    """ Protected static methods """

    @staticmethod
    def _get_client():
        """
        :rtype: SqlmapClient
        """
        if SqlmapClient._client is None:
            SqlmapClient._client = SqlmapClient()
        return SqlmapClient._client

    @staticmethod
    def _task_new() -> SqlmapTask:
        """
        :return: The new task
        """
        client = SqlmapClient._get_client()
        return SqlmapTask.task_new(client.base_url)
