import os, datetime, calendar
from termcolor import colored
from . import storage
from app.env import APP_LOGFILE, APP_PROC, DEBUG

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

    # info
    def inf(self, msg):
        self.__log__(msg, 'INFO ', 'cyan')

    # error
    def err(self, msg):
        self.__log__(msg, 'ERROR', 'red')

    # success
    def suc(self, msg):
        self.__log__(msg, 'DONE ', 'green')

    def __log__(self, msg, type, color):
        self.__check_log_file__()
        msg_log = self.__get_log_header__()+' '+colored(type, color)+' : '+msg.rstrip()
        if (DEBUG): print(msg_log)
        storage.append_in_file(msg_log, APP_LOGFILE)

    def __check_log_file__(self):
        storage.check_folder(os.path.dirname(APP_LOGFILE))
        # Se il file di log pesa almeno 5 MB, lo sovrascrivo
        if (os.path.isfile(APP_LOGFILE)):
            size_file_mb = os.stat(APP_LOGFILE).st_size / 1000000.0
            if size_file_mb >= 5:
                storage.delete(APP_LOGFILE)

    def __get_timestamp__(self):
        now_month = int(datetime.datetime.now().strftime("%m"))
        timestamp = calendar.month_abbr[now_month] + ' ' + datetime.datetime.now().strftime("%d %H:%M:%S")
        return timestamp

    def __get_log_header__(self):
        return self.__get_timestamp__() + ' ' + APP_PROC
