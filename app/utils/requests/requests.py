"""
*********************************************************************************
*                                                                               *
* requests.py -- Methods to make single and multiple requests.                  *
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

import json
import requests
import simplejson

from app.env import APP_VERSION, APP_NAME
from app.env_local import APP_DEBUG
from app.utils.helpers.logger import Log
from app.utils.helpers.validators import is_url


# Request Types
class Type:
    GET = 'get'
    POST = 'get'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'

    @staticmethod
    def all():
        return Type.GET, Type.POST, Type.PUT, Type.PATCH, Type.DELETE


def print_request(_request, limit=1000):
    Log.info(str(_request.url))
    Log.info('      |--- status_code: ' + str(_request.status_code))
    Log.info('      |--- encoding: ' + str(_request.encoding))
    Log.info('      |--- headers:')
    for key, value in _request.headers.items():
        Log.info('      |       |--- ' + str(key) + ': ' + str(value))
    Log.info('      |')
    try:
        json_body = _request.json()
        Log.info('      |-- data: ' + str(json_body))
    except ValueError:
        data = str(_request.text)
        if len(data) > limit:
            data = '[truncated]' + data[0:limit]
        Log.info('      |-- data: ' + data)


# Effettua una richiesta verso l'url passato
# @param url un url
# @param request_type get|post|put|patch|delete
# @param data dizionario con parametri
def request(url, request_type=Type.GET, data=None, headers=None):
    if headers is None:
        headers = {}
    req_headers = {
        'User-Agent': str(APP_NAME)+' '+str(APP_VERSION)
    }
    req_headers.update(headers)
    if data is None:
        data = {}
    request_type = request_type.lower()
    if not is_url(url):
        Log.error(str(url) + ' is not a valid url!')
        return None
    try:
        if request_type == Type.GET:
            r = requests.get(url, data, headers=req_headers)
        elif request_type == Type.POST:
            r = requests.post(url, data, headers=req_headers)
        elif request_type == Type.PUT:
            r = requests.put(url, data, headers=req_headers)
        elif request_type == Type.PATCH:
            r = requests.patch(url, data, headers=req_headers)
        elif request_type == Type.DELETE:
            r = requests.delete(url, headers=req_headers)
        else:
            Log.error(str(request_type) + ' is not a valid request type!')
            return None
        if APP_DEBUG:
            print_request(r)
        return r
    except requests.exceptions.ConnectionError or requests.exceptions.TooManyRedirects as e:
        Log.error('Unable to connect to ' + str(url))
        Log.error('Exception: ' + str(e))
    return None


# Effettua una richiesta verso più urls in modo sequenziale
# @param urls una lista di url
# @param request_type get|post|put|patch|delete
# @param data dizionario con parametri
def multi_request(urls, request_type=Type.GET, data=None, headers=None):
    if APP_DEBUG:
        Log.info('CALLED: multi_request(' + str(urls) + ', ' + str(request_type) + ', ' + str(data) + ')')
    request_type = request_type.lower()
    for url in urls:
        r = request(url, request_type, data, headers)
        if r is None:
            continue
        if APP_DEBUG:
            try:
                print(r.json())
            except json.decoder.JSONDecodeError or simplejson.errors.JSONDecodeError:
                print(r.text)
