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

from black_widow.app.env import APP_VERSION, APP_NAME, APP_DEBUG
from black_widow.app.services import Log
from black_widow.app.helpers.validators import is_url


class HttpRequest:
    """
    HttpRequest Manager
    """

    DEFAULT_TIMEOUT = 30    # seconds

    class Type:
        """ Request Types """
        GET = 'get'
        POST = 'post'
        PUT = 'put'
        PATCH = 'patch'
        DELETE = 'delete'

        @staticmethod
        def all() -> tuple:
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
            headers: dict = None,
            timeout: int = DEFAULT_TIMEOUT,
            cookies: str or dict = None
    ) -> requests.Response or None:
        """
        Make a request to chosen url
        :param url: The target url
        :param request_type: get|post|put|patch|delete
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`
        :param json: (optional) json data to send in the body of the :class:`Request`
        :param headers: The headers to send
        :param timeout: The request timeout
        :param cookies: The request cookies
        :return The response of request, or None (if the request fail)
        """
        if headers is None:
            headers = {}
        if type(cookies) is str:
            try:
                cookies = dict((k.strip(), v.strip()) for k, v in (c.split('=') for c in cookies.split(';')))
            except ValueError:
                # Wrong or empty cookies
                cookies = None
                pass

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
                response = requests.get(url, data, headers=req_headers, timeout=timeout, cookies=cookies)
            elif request_type == HttpRequest.Type.POST:
                response = requests.post(url, data, json, headers=req_headers, timeout=timeout, cookies=cookies)
            elif request_type == HttpRequest.Type.PUT:
                response = requests.put(url, data, headers=req_headers, timeout=timeout, cookies=cookies)
            elif request_type == HttpRequest.Type.PATCH:
                response = requests.patch(url, data, headers=req_headers, timeout=timeout, cookies=cookies)
            elif request_type == HttpRequest.Type.DELETE:
                response = requests.delete(url, headers=req_headers, timeout=timeout, cookies=cookies)
            else:
                Log.error(str(request_type) + ' is not a valid request type!')
                return None
            if APP_DEBUG:
                HttpRequest.print_response(response)
            return response
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.TooManyRedirects,
                requests.exceptions.ReadTimeout
        ) as e:
            Log.error('Unable to complete request to ' + str(url))
            Log.error('Exception: ' + str(e))
        return None

    @staticmethod
    def multi_sequential_requests(
            urls: list,
            request_type: str = Type.GET,
            data=None,
            json: dict or list = None,
            headers: dict = None
    ) -> dict:
        """
        Make multiple sequential requests
        :param urls: The list of target urls
        :param request_type: get|post|put|patch|delete
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`
        :param json: (optional) json data to send in the body of the :class:`Request`
        :param headers: The headers to send
        :return A dictionary of responses like {'url_1': <response>, 'url_2': <response>, ...}
        """
        if APP_DEBUG:
            Log.info('CALLED: multi_request(' + str(urls) + ', ' + str(request_type) + ', ' + str(data) + ')')
        request_type = request_type.lower()
        response_dict = dict()
        for url in urls:
            response = HttpRequest.request(url, request_type, data, json, headers)
            if response is None:
                continue
            response_dict[url] = response
            if APP_DEBUG:
                try:
                    print(response.json())
                except (JSONDecodeError, SimpleJSONDecodeError):
                    print(response.text)
        return response_dict

    @staticmethod
    def is_image(response: requests.Response) -> bool:
        return HttpRequest.__check_header(response, 'content-type', 'image')

    @staticmethod
    def default_agent() -> str:
        """
        :return The black-widow agent
        """
        return str(APP_NAME) + ' ' + str(APP_VERSION)

    @staticmethod
    def print_response(response, limit=1000):
        """
        :param response: The response to print
        :param limit: The limit data length before truncate that
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

    @staticmethod
    def __check_header(response: requests.Response, header: str, header_value: str) -> bool:
        if response.headers is None:
            return False
        for key, value in response.headers.items():
            key: str
            value: str
            if key.lower() != header.lower():
                continue
            return value.lower().split('/')[0] == header_value.lower()
        return False
