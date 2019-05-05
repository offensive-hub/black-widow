# APP_SETTINGS è il file json contenente i settings
from app.env import APP_SETTINGS, APP_DEBUG
from app.utils.helpers import util, validators
from app.utils.helpers.logger import Log
from app.utils.helpers.util import set_json, get_json
from app.utils.settings import keys

class Get:

    @staticmethod
    def my_ip():
        if (APP_DEBUG): Log.info('CALLED: Get.my_ip()')
        return Get.__get__(keys.MY_IP)

    @staticmethod
    def __get__(key):
        dictionary = get_json(APP_SETTINGS)
        return dictionary.get(key)
