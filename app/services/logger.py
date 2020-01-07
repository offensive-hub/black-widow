# -*- coding: utf-8 -*-

"""
*********************************************************************************
*                                                                               *
* logger.py -- The logger class for global usage.                               *
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

import calendar
import datetime
import os

from multiprocessing.process import current_process
from threading import current_thread
from termcolor import colored

from black_widow.app.env import APP_LOGFILE, APP_PROC, APP_DEBUG
from black_widow.app.helpers import storage


# Logger
class Log:
    logger = None

    @staticmethod
    def info(msg):
        Log._log('inf', msg)

    @staticmethod
    def success(msg):
        Log._log('suc', msg)

    @staticmethod
    def error(msg):
        Log._log('err', msg)

    @staticmethod
    def warning(msg):
        Log._log('war', msg)

    @staticmethod
    def _log(method: str, msg):
        if Log.logger is None:
            Log.logger = Log()
        getattr(Log.logger, '_' + method)(str(msg))

    def __init__(self):
        storage.touch(APP_LOGFILE)
        try:
            storage.chmod(APP_LOGFILE, 0o0666)
        except PermissionError:
            pass

    # info
    def _inf(self, msg):
        self.__log__(msg, 'INFO', 'cyan')

    # error
    def _err(self, msg):
        self.__log__(msg, 'ERROR', 'red')

    # warning
    def _war(self, msg):
        self.__log__(msg, 'WARNING', 'yellow')

    # success
    def _suc(self, msg):
        self.__log__(msg, 'DONE', 'green')

    def __log__(self, msg, _type, color):
        self._check_log_file()
        msg_log = self._get_log_header() + ' ' + colored(_type, color)
        curr_process = current_process()
        curr_thread = current_thread()
        if 'Main' not in curr_process.name:
            msg_log += ' [' + curr_process.name + ']'
        if 'Main' not in curr_thread.name:
            msg_log += ' (' + curr_thread.name + ')'
        msg_log += ': ' + msg.rstrip()
        if APP_DEBUG:
            print(msg_log)
        storage.append_in_file(msg_log, APP_LOGFILE)

    def _get_log_header(self):
        return self._get_timestamp() + ' ' + APP_PROC

    @staticmethod
    def _check_log_file():
        storage.check_folder(os.path.dirname(APP_LOGFILE))
        # Se il file di log pesa almeno 5 MB, lo sovrascrivo
        if os.path.isfile(APP_LOGFILE):
            try:
                size_file_mb = os.stat(APP_LOGFILE).st_size / 1000000.0
                if size_file_mb >= 5:
                    storage.delete(APP_LOGFILE)
            except FileNotFoundError:
                # Un altro thread o processo ha già eliminato il file
                return

    @staticmethod
    def _get_timestamp():
        now_month = int(datetime.datetime.now().strftime("%m"))
        timestamp = calendar.month_abbr[now_month] + ' ' + datetime.datetime.now().strftime("%d %H:%M:%S")
        return timestamp
