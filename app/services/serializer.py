"""
*********************************************************************************
*                                                                               *
* serializer.py -- The serializer classes for global usage.                     *
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

import json
import os
import pickle

from black_widow.app.helpers import storage


class PickleSerializer:
    """ The black-widow PickleSerializer """

    @staticmethod
    def get_object(file: str):
        """
        :param file: A file that contains a dumped object
        :return:
        """
        if not os.path.isfile(file):
            return None
        f = open(file, 'rb')
        obj = pickle.load(f)
        f.close()
        return obj

    @staticmethod
    def set_object(obj, file: str):
        """
        :param obj: The object to dump in file
        :param file: The file where dumps the object
        """
        f = open(file, 'wb')
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def add_item_to_dict(key, value, file: str):
        """
        :param key: The dictionary key
        :param value: The dictionary value
        :param file: The file where dictionary is dumped
        """
        dictionary = PickleSerializer.get_object(file)
        if type(dictionary) != dict:
            dictionary = dict()
        dictionary[key] = value
        PickleSerializer.set_object(dictionary, file)


class JsonSerializer:
    """ The black-widow JsonSerializer """

    @staticmethod
    def get_dictionary(file: str) -> dict:
        """
        :param file: A file that contains a json
        :return: A dictionary
        """
        if not os.path.isfile(file):
            return dict()
        return JsonSerializer.load_json(storage.read_file(file))

    @staticmethod
    def set_dictionary(dictionary: dict, file: str):
        """
        :param dictionary: The dictionary to dump in file
        :param file: The file where dumps the object
        """
        dumped_json = JsonSerializer.dump_json(dictionary)
        storage.overwrite_file(dumped_json, file)

    @staticmethod
    def add_item_to_dict(key, value, file: str):
        """
        :param key: The dictionary key or None
        :param value: The dictionary value
        :param file: The file where dictionary is dumped
        """
        dictionary = JsonSerializer.get_dictionary(file)
        if key is None:
            key = len(dictionary)
        dictionary[key] = value
        JsonSerializer.set_dictionary(dictionary, file)

    @staticmethod
    def dump_json(obj) -> str:
        """
        :type obj: dict or list
        :return: The dumped json of object
        """
        try:
            return json.dumps(obj)
        except json.decoder.JSONDecodeError:
            return ""

    @staticmethod
    def load_json(string: str) -> dict:
        """
        :param string: The string to transform in json
        :return: A dictionary
        """
        try:
            return json.loads(string)
        except json.decoder.JSONDecodeError:
            return dict()
