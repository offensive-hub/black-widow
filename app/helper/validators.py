# -*- coding: utf-8 -*-

"""
*********************************************************************************
*                                                                               *
* validators.py -- Validation methods.                                          *
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

import re

from app.helper.util import regex_is_string


# @return True se il parametro passato e' un ip address, False altrimenti
def is_ip(ip_address):
    if type(ip_address) != str:
        return False
    regex = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    reg = re.compile(regex)
    return reg.match(ip_address) is not None


# @return True se il parametro passato e' un mac address, False altrimenti
def is_mac(mac_address):
    if type(mac_address) != str:
        return False
    regex = '^\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}$'
    reg = re.compile(regex)
    return reg.match(mac_address) is not None


# @return True se il parametro passato è un url valido, False altrimenti
def is_url(url):
    if type(url) != str:
        return False
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.match(url):
        return True
    return False


def is_hex(text: str) -> bool:
    """
    Check if the input text is an hexadecimal value
    :param text: The text to check
    :return: True, if text is an hexadecimal value, otherwise False
    """
    return regex_is_string('^0x[A-Fa-f0-9]+$', text)


def is_int(text: str) -> bool:
    """
    Check if the input text is a decimal value
    :param text: The text to check
    :return: True, if text is an decimal value, otherwise False
    """
    return regex_is_string('^[0-9]+$', text)
