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

from sqlmap.lib.utils.api import server as sqlmap_server
from time import sleep

from black_widow.app.managers.request import HttpRequest
from black_widow.app.services import Log, MultiTask
from black_widow.app.helpers.network import check_socket
from black_widow.app.helpers.util import rand_str

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
    def try_inject_url(
            url: str,
            cookies: str = '',
            delay: int = 1,
            random_agent: bool = False
    ) -> SqlmapTask:
        task_options = {
            'dbms': 'MySQL',
            'cookie': cookies,
            'referer': url,
            'delay': delay,
            'randomAgent': random_agent,
            'url': url,
        }
        sqlmap_task = SqlmapClient._task_new()
        sqlmap_task.option_set(task_options)
        sqlmap_task.scan_start()
        return sqlmap_task

    @staticmethod
    def try_inject_forms(
            forms: dict,
            cookies: str = '',
            delay: int = 1,
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
            page_forms: dict    # The forms in page returned by url
            if page_forms.get('tag') == 'form':
                page_forms_in_loop = {
                    0: page_forms
                }
            else:
                page_forms_in_loop = page_forms
            # noinspection PyUnusedLocal
            for page_form in page_forms_in_loop.values():
                page_form: dict    # The attributes and inputs of form
                page_form_attrs = page_form.get('attrs')
                action: str = page_form_attrs.get('action')
                method: str = page_form_attrs.get('method')
                inputs: dict = page_form.get('children')

                if random_agent:
                    agent = None
                else:
                    agent = HttpRequest.default_agent()

                task_options = {
                    'dbms': 'MySQL',
                    'cookie': cookies,
                    'agent': agent,
                    'referer': url,
                    'delay': delay,
                    'randomAgent': random_agent,
                    'method': method,
                    'url': action,
                    'data': SqlmapClient.__get_data(inputs)
                }

                csrf_token = SqlmapClient.__get_csrf_token(inputs)
                if csrf_token is not None:
                    csrf_token_name = csrf_token.get('name')
                    task_options.update({
                        'csrfUrl': url,
                        'csrfMethod': HttpRequest.Type.GET,
                        'csrfToken': csrf_token_name,
                    })

                # for key, value in task_options.items():
                #     print('---------- ' + key + ': ----------')
                #     print(value)

                sqlmap_task = SqlmapClient._task_new()
                sqlmap_task.option_set(task_options)
                sqlmap_tasks[sqlmap_task.id] = sqlmap_task

                sqlmap_task.scan_start()

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

    @staticmethod
    def __get_csrf_token(inputs: dict) -> dict:
        csrf_field = None
        for name, input_field in inputs.items():
            if input_field.get('type') != 'hidden':
                continue
            name_lower: str = name.lower()
            if 'csrf' in name_lower:
                return input_field
            if 'token' in name_lower:
                csrf_field = input_field
        return csrf_field

    @staticmethod
    def __get_data(inputs: dict) -> str:
        data = ''
        for input_field in inputs.values():
            input_attrs = input_field.get('attrs')
            input_name: str = input_attrs.get('name')
            if input_name is None:
                continue
            input_type: str = input_attrs.get('type')
            input_value: str = input_attrs.get('value')
            if input_type is not None:
                input_type = input_type.lower()
            if input_value is None or input_value == '':
                if input_type == 'email':
                    input_value = 'email@example.com'
                elif type == 'password':
                    input_value = rand_str()
                else:
                    input_value = '1'
            data += input_name + '=' + input_value + '&'
        if len(data) > 0:
            # Remove last "&"
            data = data[0:-1]
        return data
