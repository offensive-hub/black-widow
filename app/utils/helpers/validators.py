# -*- coding: utf-8 -*-

"""
Funzioni per validazioni
"""

import re


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
