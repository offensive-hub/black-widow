"""
*********************************************************************************
*                                                                               *
* env.py -- Environment variables.                                              *
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

from os.path import dirname, join, isfile
from pathlib import Path

# ------- Black-widow files ------- #
APP_PATH = dirname(__file__)    # /path/to/app
ROOT_PATH = dirname(APP_PATH)   # parent of /path/to/app
PRIVATE_ENV_FILE = join(ROOT_PATH, '.env')

# ----- Editable environments ----- #
APP_DEBUG = False
APP_WEB_HOST = '127.0.0.1'
APP_WEB_PORT = 8295
APP_TMP = '/tmp/black-widow'
IGNORE_NON_ROOT = False
FLAG_REGEX = '[A-Z0-9]{31}='

EDITABLE_ENV = (
    'APP_DEBUG',
    'APP_WEB_HOST',
    'APP_WEB_PORT',
    'APP_TMP',
    'IGNORE_NON_ROOT',
    'FLAG_REGEX'
)

# ----------- Read .env ----------- #
if isfile(PRIVATE_ENV_FILE):
    with open(PRIVATE_ENV_FILE) as f:
        for e in f.readlines():
            env = e.strip()
            if len(env) < 3:
                continue
            if env[0] == '#':
                continue
            key, val = env.split('=', 1)[0:2]
            key: str = key.strip()
            val: str = val.strip()
            if len(key) == 0 or len(val) == 0:
                raise EnvironmentError("Wrong environment in .env file: " + env)
            if key not in EDITABLE_ENV:
                raise EnvironmentError("Non editable environment in .env file: " + env)
            if val[0] == "'" or val[0] == '"':
                i = 0
                val_ok = ''
                for char in val:
                    val_ok += val[i]
                    if i >= 1 and char == val[0]:
                        if val[i-1] != '\\':
                            break
                    i += 1
                val = val_ok
                if len(val) == 0:
                    raise EnvironmentError("Wrong environment in .env file: " + env)
            else:
                val = val.split('#')[0].strip()
            exec(key + ' = ' + str(val))

# ----- Derived environments ------ #
# App info
APP_VERSION = '1.7.1#beta'
APP_NAME = 'Black Widow'
APP_PROC = 'black-widow'
# App files
APP_MAIN_FILENAME = APP_PROC + '.py'
APP_LOGFILE = join(APP_TMP, APP_PROC + '.log')
# APP_STORAGE = join(APP_PATH, 'storage')
APP_STORAGE = join(str(Path.home()), '.black_widow')
APP_STORAGE_OUT = join(APP_STORAGE, 'out')
APP_WEB_ROOT = join(APP_PATH, 'gui', 'web')
APP_WEB = join(APP_WEB_ROOT, 'black_widow')
APP_SETTINGS = join(APP_STORAGE, 'settings.json')
EXEC_PATH = join(ROOT_PATH, APP_MAIN_FILENAME)
RES_PATH = join(ROOT_PATH, 'resources')
