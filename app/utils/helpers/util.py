"""
*********************************************************************************
*                                                                               *
* util.py -- Generic useful methods, used in all parts of software.             *
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
import pickle
import re
import os

from datetime import datetime

from app.env_local import APP_DEBUG
from app.utils.helpers import storage
from app.utils.helpers.logger import Log


def now():
    return str(datetime.now()).replace(' ', '_')


def timestamp():
    return str(datetime.timestamp(datetime.now()))


# @return dict Il json in formato dict
def get_json_from_string(string):
    try:
        return json.loads(string)
    except json.decoder.JSONDecodeError:
        return dict()


# @return dict Il json nel file in formato dict
def get_json(file):
    return get_json_from_string(storage.read_file(file))


# @param dictionary dict Il dizionario da scrivere nel file in formato json
def set_json(dictionary, file):
    return storage.overwrite_file(json.dumps(dictionary), file)


def append_json_item(key, value, file):
    dictionary = get_json(file)
    dictionary[key] = value
    return set_json(dictionary, file)


def get_serialized_dict(file):
    if not os.path.isfile(file):
        return dict()
    f = open(file, 'rb')
    dictionary = pickle.load(f)
    f.close()
    return dictionary


def set_serialized_dict(dictionary, file):
    f = open(file, 'wb')
    pickle.dump(dictionary, f, protocol=pickle.HIGHEST_PROTOCOL)
    f.close()


def add_serialized_dict_item(key, obj, file):
    dictionary = get_serialized_dict(file)
    dictionary[key] = obj
    set_serialized_dict(dictionary, file)


# @return True se string contiene regex
def regex_in_string(regex, string):
    if APP_DEBUG:
        Log.info('CALLED: regex_in_string(' + str(regex) + ', ' + str(string) + ')')
    reg = re.compile(regex)
    matches = re.findall(reg, string)
    return len(matches) > 0


# @return True se string ~ regex
def regex_is_string(regex, string):
    reg = re.compile(regex)
    return bool(reg.match(string))


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


def sort_dict(dictionary: dict) -> dict:
    """
    :param dictionary: The dictionary to sort
    :return: The sorted dictionary
    """
    sorted_dictionary = dict()
    i = 0
    for k in dictionary.keys():
        sorted_dictionary[i] = dictionary[k]
        i += 1
    return sorted_dictionary


def print_dict(dictionary: dict, depth: int = 0):
    """
    :type dictionary: dict
    :type depth: int
    """
    for key, value in dictionary.items():
        space = (' ' * depth) + '|-- '
        print(space + str(key) + ':')
        if type(value) is dict:
            print_dict(value, depth+1)
        else:
            print(space + ' [' + str(type(value)) + '] ' + str(value))


def pid_exists(pid: int or None) -> bool:
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


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
