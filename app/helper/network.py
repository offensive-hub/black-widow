"""
*********************************************************************************
*                                                                               *
* network.py -- Useful methods to take network info of current device.          *
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

import netifaces as ni
import socket

from contextlib import closing


def get_interfaces():
    """
    Get all network interfaces
    :rtype: list
    """
    return ni.interfaces()


def get_ip_address():
    """
    Get the current LAN ip address of this device
    :rtype: str
    """
    ip = None
    interfaces = get_interfaces()
    for interface in interfaces:
        try:
            ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            break
        except (KeyError, Exception):
            pass
    return ip


def check_socket(host: str, port: int):
    """
    Check if socket is running, so if the port is open in chosen host
    :param host: The host   (eg. 127.0.0.1)
    :param port: The port   (eg. 443)
    :rtype: bool
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0
