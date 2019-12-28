"""
*********************************************************************************
*                                                                               *
* http_request.py -- Methods to make single and multiple http requests          *
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

from json.decoder import JSONDecodeError
from simplejson.errors import JSONDecodeError as SimpleJSONDecodeError

from app.env import APP_VERSION, APP_NAME
from app.env_local import APP_DEBUG
from app.utils.helpers.logger import Log
from app.utils.helpers.validators import is_url


class HttpRequest:
    """
    Class HttpRequest
    """

    class Type:
        """ Request Types """
        GET = 'get'
        POST = 'post'
        PUT = 'put'
        PATCH = 'patch'
        DELETE = 'delete'

        @staticmethod
        def all():
            """
            :return: all supported request methods
            """
            return HttpRequest.Type.GET, \
                   HttpRequest.Type.POST, \
                   HttpRequest.Type.PUT, \
                   HttpRequest.Type.PATCH, \
                   HttpRequest.Type.DELETE

    @staticmethod
    def request(
            url: str,
            request_type: str = Type.GET,
            data=None,
            json: dict or list = None,
            headers: dict = None
    ):
        """
        Make a request to chosen url
        :param url: The target url
        :param request_type: get|post|put|patch|delete
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`
        :param json: (optional) json data to send in the body of the :class:`Request`
        :param headers: The headers to send
        :rtype: requests.Response
        """
        if headers is None:
            headers = {}
        req_headers = {
            'User-Agent': str(APP_NAME) + ' ' + str(APP_VERSION)
        }
        req_headers.update(headers)

        if data is None:
            data = {}

        request_type = request_type.lower()
        if not is_url(url):
            Log.error(str(url) + ' is not a valid url!')
            return None
        try:
            if request_type == HttpRequest.Type.GET:
                r = requests.get(url, data, headers=req_headers)
            elif request_type == HttpRequest.Type.POST:
                r = requests.post(url, data, json, headers=req_headers)
            elif request_type == HttpRequest.Type.PUT:
                r = requests.put(url, data, headers=req_headers)
            elif request_type == HttpRequest.Type.PATCH:
                r = requests.patch(url, data, headers=req_headers)
            elif request_type == HttpRequest.Type.DELETE:
                r = requests.delete(url, headers=req_headers)
            else:
                Log.error(str(request_type) + ' is not a valid request type!')
                return None
            if APP_DEBUG:
                HttpRequest.print_response(r)
            return r
        except requests.exceptions.ConnectionError or requests.exceptions.TooManyRedirects as e:
            Log.error('Unable to connect to ' + str(url))
            Log.error('Exception: ' + str(e))
        return None

    @staticmethod
    def multi_sequential_requests(
            urls: list,
            request_type: str = Type.GET,
            data=None,
            json: dict or list = None,
            headers: dict = None
    ):
        """
        Make multiple sequential requests
        :param urls: The list of target urls
        :param request_type: get|post|put|patch|delete
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`
        :param json: (optional) json data to send in the body of the :class:`Request`
        :param headers: The headers to send
        :rtype: list
        """
        if APP_DEBUG:
            Log.info('CALLED: multi_request(' + str(urls) + ', ' + str(request_type) + ', ' + str(data) + ')')
        request_type = request_type.lower()
        r_list = []
        for url in urls:
            r = HttpRequest.request(url, request_type, data, json, headers)
            if r is None:
                continue
            r_list.append(r)
            if APP_DEBUG:
                try:
                    print(r.json())
                except JSONDecodeError or SimpleJSONDecodeError:
                    print(r.text)
        return r_list

    @staticmethod
    def default_agent() -> str:
        """
        :return: The black-widow agent
        """
        return str(APP_NAME) + ' ' + str(APP_VERSION)

    @staticmethod
    def print_response(response, limit=1000):
        """
        :param response: The response to print
        :param limit:
        """
        Log.info(str(response.url))
        Log.info('      |--- status_code: ' + str(response.status_code))
        Log.info('      |--- encoding: ' + str(response.encoding))
        Log.info('      |--- headers:')
        for key, value in response.headers.items():
            Log.info('      |       |--- ' + str(key) + ': ' + str(value))
        Log.info('      |')
        try:
            json_body = response.json()
            Log.info('      |-- data: ' + str(json_body))
        except ValueError:
            data = str(response.text)
            if len(data) > limit:
                data = '[truncated]' + data[0:limit]
            Log.info('      |-- data: ' + data)
