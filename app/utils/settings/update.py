"""
*********************************************************************************
*                                                                               *
* update.py -- Methods to update the json file ``APP_SETTINGS``.                *
*                                                                               *
********************** IMPORTANT BLACK-WIDOW LICENSE TERMS **********************
*                                                                               *
* This file is part of black-widow.                                             *
*                                                                               *
* black-widow is free software: you can redistribute it and/or modify           *
* it under the terms of the GNU General Public License as published by          *
* the Free Software Foundation, either version 3 of the License, or             *
* (at your option) any later version.                                           *
*                                                                               *
* black-widow is distributed in the hope that it will be useful,                *
* but WITHOUT ANY WARRANTY; without even the implied warranty of                *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 *
* GNU General Public License for more details.                                  *
*                                                                               *
* You should have received a copy of the GNU General Public License             *
* along with black-widow.  If not, see <http://www.gnu.org/licenses/>.          *
*                                                                               *
*********************************************************************************
"""

from black_widow.app.env import APP_SETTINGS, APP_DEBUG   # Json file
from black_widow.app.services import Log, JsonSerializer
from black_widow.app.helpers import validators

from . import keys


class Set:
    @staticmethod
    def my_ip(ip):
        if APP_DEBUG:
            Log.info('CALLED: Set.my_ip(' + str(ip) + ')')
        if not validators.is_ip(ip):
            Log.error(str(ip) + ' is not a valid ip address')
            return False
        return Set.__set__(keys.MY_IP, ip)

    @staticmethod
    def my_interface(interface):
        if APP_DEBUG:
            Log.info('CALLED: Set.my_interface(' + str(interface) + ')')
        return Set.__set__(keys.MY_INTERFACE, interface)

    @staticmethod
    def team_token(token):
        if APP_DEBUG:
            Log.info('CALLED: Set.team_token(' + str(token) + ')')
        return Set.__set__(keys.TEAM_TOKEN, token)

    @staticmethod
    def submit_url(url):
        if APP_DEBUG:
            Log.info('CALLED: Set.submit_url(' + str(url) + ')')
        if not validators.is_url(url):
            Log.error(str(url) + ' is not a valid url')
            return False
        return Set.__set__(keys.SUBMIT_URL, url)

    @staticmethod
    def game_server(ip):
        if APP_DEBUG:
            Log.info('CALLED: Set.game_server(' + str(ip) + ')')
        if not validators.is_ip(ip):
            Log.error(str(ip) + ' is not a valid ip address')
            return False
        return Set.__set__(keys.GAME_SERVER, ip)

    @staticmethod
    def flag_regex(regex):
        if APP_DEBUG:
            Log.info('CALLED: Set.flag_regex(' + str(regex) + ')')
        return Set.__set__(keys.FLAG_REGEX, regex)

    @staticmethod
    def __set__(key, value):
        dictionary = JsonSerializer.get_dictionary(APP_SETTINGS)
        dictionary[key] = value
        JsonSerializer.set_dictionary(dictionary, APP_SETTINGS)
        return True


# Add - Per gestire parametri di tipo lista
class Add:
    @staticmethod
    def server_to_attack(ip):
        if APP_DEBUG:
            Log.info('CALLED: Add.server_to_attack(' + str(ip) + ')')
        if not validators.is_ip(ip):
            Log.error(str(ip) + ' is not a valid ip address')
            return False
        return Add.__add__(keys.SERVER_TO_ATTACK, ip)

    @staticmethod
    def server_to_defend(ip):
        if APP_DEBUG:
            Log.info('CALLED: Add.server_to_defend(' + str(ip) + ')')
        if not validators.is_ip(ip):
            Log.error(str(ip) + ' is not a valid ip address')
            return False
        return Add.__add__(keys.SERVER_TO_DEFEND, ip)

    @staticmethod
    def team_player(ip):
        if APP_DEBUG:
            Log.info('CALLED: Add.team_player(' + str(ip) + ')')
        if not validators.is_ip(ip):
            Log.error(str(ip) + ' is not a valid ip address')
            return False
        return Add.__add__(keys.TEAM_PLAYER, ip)

    # Aggiunge un elemento da una lista
    @staticmethod
    def __add__(key, element):
        dictionary = JsonSerializer.get_dictionary(APP_SETTINGS)
        elements = dictionary.get(key)
        if type(elements) != list:
            elements = []
        if element not in elements:
            elements.append(element)
            dictionary[key] = elements
            JsonSerializer.set_dictionary(dictionary, APP_SETTINGS)
        return True


class Remove:
    @staticmethod
    def my_ip():
        if APP_DEBUG:
            Log.info('CALLED: Remove.my_ip()')
        return Set.__set__(keys.MY_IP, None)

    @staticmethod
    def my_interface():
        if APP_DEBUG:
            Log.info('CALLED: Remove.my_interface()')
        return Set.__set__(keys.MY_INTERFACE, None)

    @staticmethod
    def team_token():
        if APP_DEBUG:
            Log.info('CALLED: Remove.team_token()')
        return Set.__set__(keys.TEAM_TOKEN, None)

    @staticmethod
    def game_server():
        if APP_DEBUG:
            Log.info('CALLED: Remove.game_server()')
        return Set.__set__(keys.GAME_SERVER, None)

    @staticmethod
    def submit_url():
        if APP_DEBUG:
            Log.info('CALLED: Remove.submit_url()')
        return Set.__set__(keys.SUBMIT_URL, None)

    @staticmethod
    def flag_regex():
        if APP_DEBUG:
            Log.info('CALLED: Remove.flag_regex()')
        return Set.__set__(keys.FLAG_REGEX, None)

    @staticmethod
    def server_to_attack(ip='*'):
        if APP_DEBUG:
            Log.info('CALLED: Remove.server_to_attack(' + str(ip) + ')')
        if ip != '*' and not validators.is_ip(ip):
            Log.error(str(ip) + ' is not a valid ip address')
            return False
        return Remove.__remove__(keys.SERVER_TO_ATTACK, ip)

    @staticmethod
    def server_to_defend(ip='*'):
        if APP_DEBUG:
            Log.info('CALLED: Remove.server_to_defend(' + str(ip) + ')')
        if ip != '*' and not validators.is_ip(ip):
            Log.error(str(ip) + ' is not a valid ip address')
            return False
        return Remove.__remove__(keys.SERVER_TO_DEFEND, ip)

    @staticmethod
    def team_player(ip='*'):
        if APP_DEBUG:
            Log.info('CALLED: Remove.team_player(' + str(ip) + ')')
        if ip != '*' and not validators.is_ip(ip):
            Log.error(str(ip) + ' is not a valid ip address')
            return False
        return Remove.__remove__(keys.TEAM_PLAYER, ip)

    # Rimuove un elemento da una lista
    @staticmethod
    def __remove__(key, element):
        dictionary = JsonSerializer.get_dictionary(APP_SETTINGS)
        if dictionary.get(key) is None:
            return True
        if element == '*':
            # Rimuove tutti gli elementi
            dictionary[key] = []
            JsonSerializer.set_dictionary(dictionary, APP_SETTINGS)
            return True
        elements = dictionary[key]
        if element in elements:
            elements.remove(element)
            dictionary[key] = elements
            JsonSerializer.set_dictionary(dictionary, APP_SETTINGS)
        return True


class Get:
    @staticmethod
    def all():
        if APP_DEBUG:
            Log.info('CALLED: Get.all()')
        return Get.__get__()

    @staticmethod
    def my_ip():
        if APP_DEBUG:
            Log.info('CALLED: Get.my_ip()')
        return Get.__get__(keys.MY_IP)

    @staticmethod
    def my_interface():
        if APP_DEBUG:
            Log.info('CALLED: Get.my_interface()')
        return Get.__get__(keys.MY_INTERFACE)

    @staticmethod
    def team_token():
        if APP_DEBUG:
            Log.info('CALLED: Get.team_token()')
        return Get.__get__(keys.TEAM_TOKEN)

    @staticmethod
    def game_server():
        if APP_DEBUG:
            Log.info('CALLED: Get.game_server()')
        return Get.__get__(keys.GAME_SERVER)

    @staticmethod
    def submit_url():
        if APP_DEBUG:
            Log.info('CALLED: Get.submit_url()')
        return Get.__get__(keys.SUBMIT_URL)

    @staticmethod
    def server_to_attack():
        if APP_DEBUG:
            Log.info('CALLED: Get.server_to_attack()')
        return Get.__get__(keys.SERVER_TO_ATTACK)

    @staticmethod
    def flag_regex():
        if APP_DEBUG:
            Log.info('CALLED: Get.flag_regex()')
        return Get.__get__(keys.FLAG_REGEX)

    @staticmethod
    def __get__(key=None):
        dictionary = JsonSerializer.get_dictionary(APP_SETTINGS)
        if key is None:
            return dictionary
        return dictionary.get(key)
