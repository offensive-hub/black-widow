import os, datetime, calendar
from termcolor import colored
from threading import current_thread
from multiprocessing.process import current_process
from . import storage
from app.env import APP_LOGFILE, APP_PROC, APP_DEBUG

# Logger
class Log:
    logger = None

    @staticmethod
    def info(msg):
        if (Log.logger == None): Log.logger = Log()
        Log.logger.inf(str(msg))

    @staticmethod
    def success(msg):
        if (Log.logger == None): Log.logger = Log()
        Log.logger.suc(str(msg))

    @staticmethod
    def error(msg):
        if (Log.logger == None): Log.logger = Log()
        Log.logger.err(str(msg))

    @staticmethod
    def warning(msg):
        if (Log.logger == None): Log.logger = Log()
        Log.logger.war(str(msg))

    # info
    def inf(self, msg):
        self.__log__(msg, 'INFO', 'cyan')

    # error
    def err(self, msg):
        self.__log__(msg, 'ERROR', 'red')

    # warning
    def war(self, msg):
        self.__log__(msg, 'WARNING', 'yellow')

    # success
    def suc(self, msg):
        self.__log__(msg, 'DONE', 'green')

    def __log__(self, msg, type, color):
        self.__check_log_file__()
        msg_log = self.__get_log_header__()+' '+colored(type, color)
        curr_process = current_process()
        curr_thread = current_thread()
        if ('Main' not in curr_process.name):
            msg_log += ' ['+curr_process.name+']'
        if ('Main' not in curr_thread.name):
            msg_log += ' ('+curr_thread.name+')'
        msg_log += ': '+msg.rstrip()
        if (APP_DEBUG): print(msg_log)
        storage.append_in_file(msg_log, APP_LOGFILE)

    def __check_log_file__(self):
        storage.check_folder(os.path.dirname(APP_LOGFILE))
        # Se il file di log pesa almeno 5 MB, lo sovrascrivo
        if (os.path.isfile(APP_LOGFILE)):
            try:
                size_file_mb = os.stat(APP_LOGFILE).st_size / 1000000.0
                if size_file_mb >= 5: storage.delete(APP_LOGFILE)
            except FileNotFoundError as e:
                # Un altro thread o processo ha già eliminato il file
                return

    def __get_timestamp__(self):
        now_month = int(datetime.datetime.now().strftime("%m"))
        timestamp = calendar.month_abbr[now_month] + ' ' + datetime.datetime.now().strftime("%d %H:%M:%S")
        return timestamp

    def __get_log_header__(self):
        return self.__get_timestamp__() + ' ' + APP_PROC
