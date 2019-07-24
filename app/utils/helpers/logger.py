# -*- coding: utf-8 -*-

import calendar
import datetime
import os
from multiprocessing.process import current_process
from threading import current_thread

from termcolor import colored

from app.env import APP_LOGFILE, APP_PROC
from app.env_local import APP_DEBUG
from app.utils.helpers import storage


# Logger
class Log:
    logger = None

    @staticmethod
    def info(msg):
        if Log.logger is None:
            Log.logger = Log()
        Log.logger._inf(str(msg))

    @staticmethod
    def success(msg):
        if Log.logger is None:
            Log.logger = Log()
        Log.logger._suc(str(msg))

    @staticmethod
    def error(msg):
        if Log.logger is None:
            Log.logger = Log()
        Log.logger._err(str(msg))

    @staticmethod
    def warning(msg):
        if Log.logger is None:
            Log.logger = Log()
        Log.logger._war(str(msg))

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
