from os.path import dirname, realpath

# Environment variables

APP_VERSION = '1.0.0#alpha'
APP_DEBUG = True
APP_NAME = 'Black Widow'
APP_PROC = 'black-widow'
APP_PATH = dirname(realpath(__file__))  # /path/to/app
APP_STORAGE = APP_PATH + '/storage'
APP_STORAGE_OUT = APP_STORAGE + '/out'
APP_SETTINGS = APP_STORAGE + '/settings.json'
APP_TMP = '/tmp/black-widow'
APP_LOGFILE = APP_TMP + '/black-widow.log'

APP_WEB_PACKAGE = 'app.gui.web'
APP_WEB_HOST = '0.0.0.0'
APP_WEB_PORT = 8000

ROOT_PATH = dirname(APP_PATH)
EXEC_PATH = ROOT_PATH + '/' + APP_PROC + '.py'
RES_PATH = ROOT_PATH + '/resources'

FLAG_REGEX = '[A-Z0-9]{31}='  # Default flag regex
