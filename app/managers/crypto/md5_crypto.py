"""
*********************************************************************************
*                                                                               *
* md5_crypto.py -- Md5 Encryption/Decryption manager                            *
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

import hashlib
import json

from black_widow.app.managers.request import HttpRequest
from black_widow.app.services import Log


class Md5Crypto:
    """
    Md5Crypto Manager
    """

    class Api:
        """
        Md5 APIs
        """

        # Method to get response data from 1st API
        @staticmethod
        def _api_1_result(json_dict):
            return json_dict.get('result')
        _api_1 = {'url': 'https://md5.pinasthika.com/api/decrypt?value=', 'get_result': _api_1_result}

        # Method to get response data from 2nd API
        @staticmethod
        def _api_2_result(json_dict):
            return json_dict[0].get('decrypted')
        _api_2 = {'url': 'https://www.md5.ovh/index.php?result=json&md5=', 'get_result': _api_2_result}

        @staticmethod
        def all():
            return Md5Crypto.Api._api_1, Md5Crypto.Api._api_2

    @staticmethod
    def encrypt(text: str):
        m = hashlib.md5()
        m.update(text.encode())
        return str(m.hexdigest())

    @staticmethod
    def decrypt(text: str):
        for api in Md5Crypto.Api.all():
            r = HttpRequest.request(api['url'] + text)
            if r is None:
                continue

            try:
                r_json = r.json()
            except json.decoder.JSONDecodeError:
                continue

            result = api['get_result'](r_json)
            if result is not None:
                return result
        Log.error('md5: unable to decrypt: ' + text)
        return None
