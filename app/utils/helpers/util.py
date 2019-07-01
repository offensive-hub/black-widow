"""
Funzioni generiche, utili in tutte le parti del software.
"""

import json
import re

from datetime import datetime

from app.env import APP_DEBUG
from app.utils.helpers import storage
from app.utils.helpers.logger import Log


def now():
    return str(datetime.now()).replace(' ', '_')


# @return dict Il json nel file in formato dict
def get_json(file):
    return get_json_str(storage.read_file(file))


# @return dict Il json in formato dict
def get_json_str(string):
    try:
        return json.loads(string)
    except json.decoder.JSONDecodeError:
        return dict()


# @param dictionary dict Il dizionario da scrivere nel file in formato json
def set_json(dictionary, file):
    return storage.overwrite_file(json.dumps(dictionary), file)


# @return True se string contiene regex
def regex_in_string(regex, string):
    if APP_DEBUG:
        Log.info('CALLED: regex_in_string(' + str(regex) + ', ' + str(string) + ')')
    reg = re.compile(regex)
    matches = re.findall(reg, string)
    return len(matches) > 0


# @param regex la regex da trovare in string
# @param replace la stringa con cui sostituire la regex
# @param string la stringa in cui trovare la regex
# @return la string passata per argomento (find), con la sostituzione
def replace_regex(regex, replace, string):
    return re.sub(regex, replace, string, flags=re.M)


# @param element Un oggetto
# @return True se element è un elemento listabile, False altrimenti
def is_listable(obj):
    return type(obj) in (list, tuple, dict, range)


# Fa eseguire al sistema operativo i comandi in args
# @param *args "cmd [argomenti]"        // ES: "netstat -tuan"
def pexec(*args):
    if APP_DEBUG:
        Log.info('CALLED: pexec' + str(args))
    """
    try:
        p=subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        Log.error(str(e))
        return []
    list_stdout=[]
    for line in p.stdout.readlines():
        list_stdout.append(str(line.decode('utf-8')).rstrip('\n'))
    return list_stdout
    """
