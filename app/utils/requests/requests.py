"""
Metodi per effettuare richieste multiple
"""

import requests, json
from app.utils.helpers.logger import Log
from app.env import APP_DEBUG

class Type:
    GET='get'
    POST='get'
    PUT='put'
    PATCH='patch'
    DELETE='delete'

def request(url, type, data={}):
    type = type.lower()
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
        else:
            Log.error("tipo "+type+" non esistente")
            return None
        return r
    except requests.exceptions.ConnectionError as e:
        Log.error('Impossibile contattare '+str(url))
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
        Log.info('Request to '+str(url))
        Log.info('      |--- status_code: '+str(r.status_code))
        Log.info('      |--- encoding: '+str(r.encoding))
        Log.info('      |--- headers:')
        for header in r.headers.keys():
            Log.info('              |--- '+header+': '+str(r.headers.get(header)))
        if (APP_DEBUG):
            try:
                print(r.json())
            except json.decoder.JSONDecodeError:
                print(r.text)
