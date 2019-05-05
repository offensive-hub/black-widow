"""
Metodi per effettuare richieste multiple
"""

import requests, json
from app.utils.helpers.logger import Log

# Effettua una richiesta verso più urls contemporaneamente
# @param urls una lista di url
def multi_request(urls, type, data):
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
        except requests.exceptions.ConnectionError as e:
            Log.error('Impossibile contattare '+str(url))
            continue
        Log.info('Request to '+str(url))
        print('status_code: '+str(r.status_code))
        print('headers: '+str(r.headers))
        print('encoding: '+str(r.encoding))
        try:
            print(r.json())
        except json.decoder.JSONDecodeError:
            print(r.text)
