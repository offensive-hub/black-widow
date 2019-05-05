"""
Funzioni generiche, utili in tutte le parti del software.
"""

import json, re
from . import storage
from app.env import APP_DEBUG
from app.utils.helpers.logger import Log

# @return dict Il json in formato dict
def get_json(file):
    try:
        return json.loads(storage.read_file(file))
    except json.decoder.JSONDecodeError:
        return dict()

# @param dictionary dict Il dizionario da scrivere nel file in formato json
def set_json(dictionary, file):
    return storage.overwrite_file(json.dumps(dictionary), file)

# @return True se string contiene regex
def regex_in_string(regex, string):
    if (APP_DEBUG): Log.info('CALLED: regex_in_string('+str(regex)+', '+str(string)+')')
    reg = re.compile(regex)
    matches = re.findall(reg, string)
    return len(matches) > 0

# Fa eseguire al sistema operativo i comandi in args
# @param *args "cmd [argomenti]"        // ES: "netstat -tuan"
def pexec(*args):
    if (APP_DEBUG): Log.info('CALLED: pexec'+str(args))
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
