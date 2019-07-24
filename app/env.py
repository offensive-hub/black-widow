from os.path import dirname, realpath

# Environment variables

APP_VERSION = '1.0.0#alpha'
APP_NAME = 'Black Widow'
APP_PROC = 'black-widow'
APP_PATH = dirname(realpath(__file__))  # /path/to/app
APP_STORAGE = APP_PATH + '/storage'
APP_WEB_ROOT = APP_PATH + '/gui/web'
APP_WEB = APP_PATH + '/gui/web/black_widow'
APP_STORAGE_OUT = APP_STORAGE + '/out'
APP_SETTINGS = APP_STORAGE + '/settings.json'
APP_TMP = '/tmp/black-widow'
APP_LOGFILE = APP_TMP + '/black-widow.log'

ROOT_PATH = dirname(APP_PATH)
EXEC_PATH = ROOT_PATH + '/' + APP_PROC + '.py'
RES_PATH = ROOT_PATH + '/resources'
