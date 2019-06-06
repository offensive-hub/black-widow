"""
Metodi per effettuare richieste multiple
"""

import requests, json
from app.utils.helpers.logger import Log
from app.utils.helpers.validators import is_url
from app.env import APP_DEBUG

# Request Types
class Type:
    GET='get'
    POST='get'
    PUT='put'
    PATCH='patch'
    DELETE='delete'
    @staticmethod
    def all():
        return (Type.GET, Type.POST, Type.PUT, Type.PATCH, Type.DELETE)

def print_request(request):
    Log.info(str(request.url))
    Log.info('      |--- status_code: '+str(request.status_code))
    Log.info('      |--- encoding: '+str(request.encoding))
    Log.info('      |--- headers:')
    for key,value in request.headers.items():
        Log.info('      |       |--- '+str(key)+': '+str(value))
    Log.info('      |')
    try:
        Log.info('      |-- data: '+str(request.json()))
    except json.decoder.JSONDecodeError:
        data = str(request.text)
        if (len(data) > 100): data = '[truncated]'+data[0:100]
        Log.info('      |-- data: '+data)

# Effettua una richiesta verso l'url passato
# @param url un url
# @param type get|post|put|patch|delete
# @param data dizionario con parametri
def request(url, type=Type.GET, data={}):
    type = type.lower()
    if (not is_url(url)):
        Log.error(str(url)+' is not a valid url!')
        return None
    if (type not in Type.all()):
        Log.error(str(type)+' is not a valid request type!')
        return None
    try:
        if (type == Type.GET):
            r = requests.get(url, data)
        elif (type == Type.POST):
            r = requests.post(url, data)
        elif (type == Type.PUT):
            r = requests.put(url, data)
        elif (type == Type.PATCH):
            r = requests.patch(url, data)
        elif (type == Type.DELETE):
            r = requests.delete(url, data)
        if (APP_DEBUG): print_request(r)
        return r
    except requests.exceptions.ConnectionError as e:
        Log.error('Impossibile contattare '+str(url))
        Log.error('Eccezzione: '+str(e))
    return None


# Effettua una richiesta verso più urls in modo sequenziale
# @param urls una lista di url
# @param type get|post|put|patch|delete
# @param data dizionario con parametri
def multi_request(urls, type, data):
    if (APP_DEBUG): Log.info('CALLED: multi('+str(urls)+', '+str(type)+', '+str(data)+')')
    type = type.lower()
    for url in urls:
        r = request(url, type, data)
        if (r == None): continue
        if (APP_DEBUG):
            try:
                print(r.json())
            except json.decoder.JSONDecodeError:
                print(r.text)
