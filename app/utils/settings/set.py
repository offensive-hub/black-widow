# APP_SETTINGS è il file json contenente i settings
from app.env import APP_SETTINGS, APP_DEBUG
from app.utils.helpers import util, validators
from app.utils.helpers.logger import Log
from app.utils.helpers.util import set_json, get_json
from app.utils.settings import keys

class Set:

    @staticmethod
    def my_ip(ip):
        if (APP_DEBUG): Log.info('CALLED: Set.my_ip('+str(ip)+')')
        if (not validators.is_ip(ip)):
            Log.error(str(ip)+' is not a valid ip address')
            return False
        return Set.__set__(keys.MY_IP, ip)

    @staticmethod
    def __set__(key, value):
        dictionary = get_json(APP_SETTINGS)
        dictionary[key] = value
        set_json(dictionary, APP_SETTINGS)
        return True
