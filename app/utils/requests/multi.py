"""
Metodi per effettuare richieste multiple
"""

import requests, json
from app.utils.helpers.logger import Log
from app.env import APP_DEBUG

# Effettua una richiesta verso più urls contemporaneamente
# @param urls una lista di url
# @param type get|post|put|patch|delete
# @param data dizionario con parametri
def multi(urls, type, data):
    if (APP_DEBUG): Log.info('CALLED: multi('+str(urls)+', '+str(type)+', '+str(data)+')')
    type = type.lower()
    for url in urls:
        try:
            if (type == 'get'):
                r = requests.get(url, data)
            elif (type == 'post'):
                r = requests.post(url, data)
            elif (type == 'put'):
                r = requests.put(url, data)
            elif (type == 'patch'):
                r = requests.patch(url, data)
            elif (type == 'delete'):
                r = requests.delete(url, data)
            else:
                Log.error("tipo "+type+" non esistente")
                return
        except requests.exceptions.ConnectionError as e:
            Log.error('Impossibile contattare '+str(url))
            continue
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
