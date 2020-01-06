"""
*********************************************************************************
*                                                                               *
* base64_crypto.py -- Base64 Encoding/Decoding manager                          *
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

from base64 import b64decode, b64encode


class Base64Crypto:
    """
    Base64Crypto Manager
    """

    @staticmethod
    def encrypt(text: str) -> str:
        return b64encode(bytes(text, encoding='utf-8')).decode('utf-8')

    @staticmethod
    def decrypt(text: str):
        return b64decode(text).decode('utf-8')
