# APP_SETTINGS è il file json contenente i settings
from app.env import APP_SETTINGS, APP_DEBUG
from app.utils.helpers import util, validators
from app.utils.helpers.logger import Log
from app.utils.helpers.util import set_json, get_json
from . import keys

class Set:
    @staticmethod
    def my_ip(ip):
        if (APP_DEBUG): Log.info('CALLED: Set.my_ip('+str(ip)+')')
        if (not validators.is_ip(ip)):
            Log.error(str(ip)+' is not a valid ip address')
            return False
        return Set.__set__(keys.MY_IP, ip)

    @staticmethod
    def game_server(ip):
        if (APP_DEBUG): Log.info('CALLED: Set.game_server('+str(ip)+')')
        if (not validators.is_ip(ip)):
            Log.error(str(ip)+' is not a valid ip address')
            return False
        return Set.__set__(keys.GAME_SERVER, ip)

    @staticmethod
    def __set__(key, value):
        dictionary = get_json(APP_SETTINGS)
        dictionary[key] = value
        set_json(dictionary, APP_SETTINGS)
        return True


# Add - Per gestire parametri di tipo lista
class Add:
    @staticmethod
    def server_to_attack(ip):
        if (APP_DEBUG): Log.info('CALLED: Add.server_to_attack('+str(ip)+')')
        if (not validators.is_ip(ip)):
            Log.error(str(ip)+' is not a valid ip address')
            return False
        return Add.__add__(keys.SERVER_TO_ATTACK, ip)

    @staticmethod
    def server_to_defend(ip):
        if (APP_DEBUG): Log.info('CALLED: Add.server_to_defend('+str(ip)+')')
        if (not validators.is_ip(ip)):
            Log.error(str(ip)+' is not a valid ip address')
            return False
        return Add.__add__(keys.SERVER_TO_DEFEND, ip)

    @staticmethod
    def team_player(ip):
        if (APP_DEBUG): Log.info('CALLED: Add.team_player('+str(ip)+')')
        if (not validators.is_ip(ip)):
            Log.error(str(ip)+' is not a valid ip address')
            return False
        return Add.__add__(keys.TEAM_PLAYER, ip)

    # Aggiunge un elemento da una lista
    @staticmethod
    def __add__(key, element):
        dictionary = get_json(APP_SETTINGS)
        elements = dictionary.get(key)
        if (type(elements) != list): elements = []
        if (element not in elements):
            elements.append(element)
            dictionary[key] = elements
            set_json(dictionary, APP_SETTINGS)
        return True


class Remove:
    @staticmethod
    def my_ip():
        if (APP_DEBUG): Log.info('CALLED: Remove.my_ip()')
        return Set.__set__(keys.MY_IP, None)

    @staticmethod
    def game_server():
        if (APP_DEBUG): Log.info('CALLED: Remove.game_server()')
        return Set.__set__(keys.GAME_SERVER, None)

    @staticmethod
    def server_to_attack(ip='*'):
        if (APP_DEBUG): Log.info('CALLED: Remove.server_to_attack('+str(ip)+')')
        if (ip != '*' and not validators.is_ip(ip)):
            Log.error(str(ip)+' is not a valid ip address')
            return False
        return Remove.__remove__(keys.SERVER_TO_ATTACK, ip)

    @staticmethod
    def server_to_defend(ip='*'):
        if (APP_DEBUG): Log.info('CALLED: Remove.server_to_defend('+str(ip)+')')
        if (ip != '*' and not validators.is_ip(ip)):
            Log.error(str(ip)+' is not a valid ip address')
            return False
        return Remove.__remove__(keys.SERVER_TO_DEFEND, ip)

    @staticmethod
    def team_player(ip='*'):
        if (APP_DEBUG): Log.info('CALLED: Remove.team_player('+str(ip)+')')
        if (ip != '*' and not validators.is_ip(ip)):
            Log.error(str(ip)+' is not a valid ip address')
            return False
        return Remove.__remove__(keys.TEAM_PLAYER, ip)

    # Rimuove un elemento da una lista
    @staticmethod
    def __remove__(key, element):
        dictionary = get_json(APP_SETTINGS)
        if (dictionary.get(key) == None): return True
        if (element == '*'):
            # Rimuove tutti gli elementi
            dictionary[key] = []
            set_json(dictionary, APP_SETTINGS)
            return True
        elements = dictionary[key]
        if (element in elements):
            elements.remove(element)
            dictionary[key] = elements
            set_json(dictionary, APP_SETTINGS)
        return True


class Get:
    @staticmethod
    def all():
        if (APP_DEBUG): Log.info('CALLED: Get.all()')
        return Get.__get__()

    @staticmethod
    def my_ip():
        if (APP_DEBUG): Log.info('CALLED: Get.my_ip()')
        return Get.__get__(keys.MY_IP)

    @staticmethod
    def game_server():
        if (APP_DEBUG): Log.info('CALLED: Get.game_server()')
        return Get.__get__(keys.GAME_SERVER)

    @staticmethod
    def server_to_attack():
        if (APP_DEBUG): Log.info('CALLED: Get.server_to_attack()')
        return Get.__get__(keys.SERVER_TO_ATTACK)

    @staticmethod
    def __get__(key=None):
        dictionary = get_json(APP_SETTINGS)
        if (key == None): return dictionary
        return dictionary.get(key)
