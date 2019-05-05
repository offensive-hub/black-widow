from os.path import dirname, realpath

# Variabili d'ambiente
DEBUG=True
APP_NAME='Black Widow'
APP_PROC='black-widow'
APP_PATH=dirname(realpath(__file__))    # /path/to/app
APP_SETTINGS=APP_PATH+'/storage/settings.json'
APP_TMP='/tmp/black-widow'
APP_LOGFILE=APP_TMP+'/black-widow.log'
