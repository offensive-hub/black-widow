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


INTERFACES = ['eth0', 'wlan0', 'usb0']


def get_ip_address():
    ip = None
    for interface in INTERFACES:
        try:
            ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            break
        except KeyError or Exception:
            pass
    return ip
