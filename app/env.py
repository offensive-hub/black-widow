"""
*********************************************************************************
*                                                                               *
* env.py -- Public environment variables.                                       *
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

from os.path import dirname, realpath

APP_VERSION = '1.3.0#alpha'
APP_NAME = 'Black Widow'
APP_PROC = 'black-widow'
APP_PATH = dirname(realpath(__file__))  # /path/to/app
APP_STORAGE = APP_PATH + '/storage'
APP_STORAGE_OUT = APP_STORAGE + '/out'
APP_WEB_ROOT = APP_PATH + '/gui/web'
APP_WEB = APP_PATH + '/gui/web/black_widow'
APP_SETTINGS = APP_STORAGE + '/settings.json'
APP_TMP = '/tmp/black-widow'
APP_LOGFILE = APP_TMP + '/black-widow.log'
ROOT_PATH = dirname(APP_PATH)
EXEC_PATH = ROOT_PATH + '/' + APP_PROC + '.py'
RES_PATH = ROOT_PATH + '/resources'
