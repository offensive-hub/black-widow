from os.path import dirname, realpath

# Variabili d'ambiente
APP_DEBUG=True
APP_NAME='Black Widow'
APP_PROC='black-widow'
APP_PATH=dirname(realpath(__file__))                # /path/to/app
APP_STORAGE=APP_PATH+'/storage'
APP_SETTINGS=APP_STORAGE+'/settings.json'
APP_TMP='/tmp/black-widow'
APP_LOGFILE=APP_TMP+'/black-widow.log'

FLAG_REGEX='[A-Z0-9]{31}='                          # Default flag regex
