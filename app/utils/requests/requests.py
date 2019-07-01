"""
Metodi per effettuare richieste multiple
"""

import json
import requests
import simplejson

from app.env import APP_DEBUG
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


def print_request(_request):
    Log.info(str(_request.url))
    Log.info('      |--- status_code: ' + str(_request.status_code))
    Log.info('      |--- encoding: ' + str(_request.encoding))
    Log.info('      |--- headers:')
    for key, value in _request.headers.items():
        Log.info('      |       |--- ' + str(key) + ': ' + str(value))
    Log.info('      |')
    try:
        Log.info('      |-- data: ' + str(_request.json()))
    except json.decoder.JSONDecodeError or simplejson.errors.JSONDecodeError:
        data = str(_request.text)
        if len(data) > 100:
            data = '[truncated]' + data[0:100]
        Log.info('      |-- data: ' + data)


# Effettua una richiesta verso l'url passato
# @param url un url
# @param request_type get|post|put|patch|delete
# @param data dizionario con parametri
def request(url, request_type=Type.GET, data=None):
    if data is None:
        data = {}
    request_type = request_type.lower()
    if not is_url(url):
        Log.error(str(url) + ' is not a valid url!')
        return None
    try:
        if request_type == Type.GET:
            r = requests.get(url, data)
        elif request_type == Type.POST:
            r = requests.post(url, data)
        elif request_type == Type.PUT:
            r = requests.put(url, data)
        elif request_type == Type.PATCH:
            r = requests.patch(url, data)
        elif request_type == Type.DELETE:
            r = requests.delete(url)
        else:
            Log.error(str(request_type) + ' is not a valid request type!')
            return None
        if APP_DEBUG:
            print_request(r)
        return r
    except requests.exceptions.ConnectionError as e:
        Log.error('Unable to connect to ' + str(url))
        Log.error('Exception: ' + str(e))
    return None


# Effettua una richiesta verso più urls in modo sequenziale
# @param urls una lista di url
# @param request_type get|post|put|patch|delete
# @param data dizionario con parametri
def multi_request(urls, request_type, data):
    if APP_DEBUG:
        Log.info('CALLED: multi(' + str(urls) + ', ' + str(request_type) + ', ' + str(data) + ')')
    request_type = request_type.lower()
    for url in urls:
        r = request(url, request_type, data)
        if r is None:
            continue
        if APP_DEBUG:
            try:
                print(r.json())
            except json.decoder.JSONDecodeError:
                print(r.text)
