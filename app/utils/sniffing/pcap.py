# -*- coding: utf-8 -*-

"""
*********************************************************************************
*                                                                               *
* pcap.py -- Packet Capture (pcap)                                              *
*                                                                               *
* Methods to sniff the network traffic through pyshark.                         *
*                                                                               *
* LayerField tree info:                                                         *
*      Field (
*                                                                               *
* pyshark repository:                                                           *
* https://github.com/KimiNewt/pyshark                                           *
*                                                                               *
* pyshark license:                                                              *
* https://raw.githubusercontent.com/KimiNewt/pyshark/master/LICENSE.txt         *
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

import pyshark

from pyshark.packet.fields import LayerField
from pyshark.packet.layer import Layer
from pyshark.packet.packet import Packet

from app.utils import settings
from app.utils.helpers.logger import Log
from app.utils.helpers.util import is_int, is_hex

from . import MacManufacturer
from . import PcapLayerField


class Pcap:
    """
    Packet Capture (pcap) class
    """
    mac_manufacturer = None

    def __init__(self, filters=None, src_file=None, dest_file=None, interface=None, limit_length=None, callback=None):
        """
        Packet capture method
        :param filters: https://wiki.wireshark.org/DisplayFilters
        :param src_file: Il file .pcap da cui leggere i pacchetti ascoltati (o None, per Live sniffing)
        :param dest_file: Il file in cui scrivere il .pcap dei pacchetti ascoltati (o None)
        :param interface: L'interfaccia da cui ascoltare (o None)
        :param limit_length: The limit length of each packet field (they will be truncated), or None
        :param callback: The callback method to call (or None)
        """
        if Pcap.mac_manufacturer is None:
            Pcap.mac_manufacturer = MacManufacturer()
        self.filters = filters
        self.src_file = src_file
        self.dest_file = dest_file
        self.limit_length = limit_length
        self.user_callback = callback
        if interface is None and src_file is None:
            self.interface = settings.Get.my_interface()
        else:
            self.interface = interface
        if src_file is not None:
            Log.info('Analyzing file: ' + src_file)
            self.capture = pyshark.FileCapture(
                input_file=src_file,
                display_filter=filters,
                output_file=dest_file,
                # include_raw=True,
                # use_json=True
                # debug=APP_DEBUG
            )
        else:
            Log.info('Analyzing live traffic')
            self.capture = pyshark.LiveCapture(
                interface=interface,
                display_filter=filters,
                output_file=dest_file,
                # include_raw=True,
                # use_json=True
                # debug=APP_DEBUG
            )
        self.capture.apply_on_packets(Pcap._callback)

    @staticmethod
    def sniff(filters=None, src_file=None, dest_file=None, interface=None, limit_length=None, callback=None):
        """
        Packet capture method
        :param filters: https://wiki.wireshark.org/DisplayFilters
        :param src_file: Il file .pcap da cui leggere i pacchetti ascoltati (o None, per Live sniffing)
        :param dest_file: Il file in cui scrivere il .pcap dei pacchetti ascoltati (o None)
        :param interface: L'interfaccia da cui ascoltare (o None)
        :param limit_length: The limit length of each packet field (they will be truncated), or None
        :param callback: The callback method to call (or None)
        :rtype: Pcap
        """
        pcap = Pcap(filters, src_file, dest_file, interface, limit_length, callback)
        return pcap

    @staticmethod
    def print_pkt_dict(pkt_dict: dict):
        """
        Print the pkt_dict
        :param pkt_dict: The pkt dict created by Pcap._callback(pkt)
        """
        for key, value in pkt_dict.items():
            if key == 'layers':
                for layer_dict in value:
                    Pcap._print_layer(layer_dict)
            elif key == 'frame_info':
                Pcap._print_layer(value)
            else:
                print(str(key) + ': ' + str(value))

    @staticmethod
    def _print_layer(layer_dict: dict):
        """
        Print the layer_dict
        :param layer_dict: The layer dict created by Pcap._callback(pkt)
        """
        print('Layer: ' + str(layer_dict.get('name')))
        for field_dict in layer_dict.get('fields'):
            Pcap._print_field(field_dict, 4)

    @staticmethod
    def _print_field(field_dict: dict, depth: int):
        """
        Print the field_dict
        :param field_dict: The field dict created by Pcap._callback(pkt)
        """
        field_header = ''
        for i in range(0, depth, 4):
            field_header += '   |'
        field_label = field_dict.get('label')
        if field_label is None:
            field_label = field_dict.get('name')
        field_key = field_header + '   |--[ ' + str(field_label) + ' ]'
        field_value = field_dict.get('value')
        if field_value is None:
            field_value = ''
        else:
            field_key += ' = '
        alternate_values = field_dict.get('alternate_values')
        if alternate_values is not None:
            field_key_len = len(field_key)
            for alternate_value in field_dict.get('alternate_values'):
                field_value += '\n' + (field_key_len * ' ') + alternate_value
        print(field_key + field_value)
        children = field_dict.get('children')
        if children is not None:
            for field_child in field_dict.get('children'):
                Pcap._print_field(field_child, depth * 2)

    # noinspection PyProtectedMember
    @staticmethod
    def _callback(pkt: Packet):
        """
        :param pkt: The pyshark packet
        :return:
        """
        pkt_dict = {
            'number': str(pkt.number),
            'captured_length': str(pkt.captured_length),
            'interface_captured': str(pkt.interface_captured),
            'highest_layer': str(pkt.highest_layer),
            'length': str(pkt.length),
            'sniff_time': str(pkt.sniff_time),
            'sniff_timestamp': str(pkt.sniff_timestamp),
            'transport_layer': str(pkt.transport_layer),
            'frame_info': Pcap._get_layer_dict(pkt.frame_info),
            'layers': []
        }
        for layer in pkt.layers:
            pkt_dict['layers'].append(Pcap._get_layer_dict(layer))
        # Pcap.print_pkt_dict(pkt_dict)
        # TODO: clean field + self.callback
        exit(0)

    # noinspection PyProtectedMember
    @staticmethod
    def _get_layer_dict(layer: Layer):
        """
        :param layer: The layer to process
        :return: The dictionary of layer
        """
        layer_dict = {
            'name': layer.layer_name,
            'fields': []
        }

        field_tree = dict()     # tree dict { name => pkt }

        def update_field_tree_keys(local_field_tree_keys: list) -> (list, dict):
            """
            Insert into the field_tree the input keys recursively
            Eg. local_field_tree_keys = ['a', 'b', 'c']
                field_tree['a']['b']['c'] = dict()
            :param local_field_tree_keys: the dictionary keys used to create the parent dicts of field
            :return: The family (as list) and the node (as dict) of field to insert
            """
            local_field_node = field_tree
            local_field_tree_family = []
            for local_field_tree_key in local_field_tree_keys:
                local_field_tree_child = local_field_node.get(local_field_tree_key)
                if local_field_tree_child is None:
                    local_field_tree_child = dict()
                    local_field_node[local_field_tree_key] = local_field_tree_child
                local_field_tree_family.insert(0, local_field_tree_child)
                local_field_node = local_field_tree_child
            return local_field_tree_family, local_field_node

        pcap_layer_field_root = PcapLayerField()

        def local_get_field_tree(local_field: LayerField):
            """
            :param local_field: The LayerField to insert in dict
            """
            field_name: str = local_field.name
            parent_poss = (int(local_field.pos), int(local_field.pos) - int(local_field.size))
            field_tree_keys = field_name.split('.')
            family, node = update_field_tree_keys(field_tree_keys)

            def find_pcap_layer_field_parent(local_member: dict, only_hex=False) -> PcapLayerField or None:
                for key, member_parent in local_member.items():
                    member_parent: PcapLayerField or dict
                    if not only_hex:
                        member_brother = None
                        if isinstance(member_parent, dict):
                            # Check brothers
                            member_brother = find_pcap_layer_field_parent(member_parent, True)
                        if member_brother is not None:
                            return member_brother
                    if key in parent_poss and member_parent.name != local_field.name:
                        if not only_hex or (is_hex(member_parent.value) and member_parent.pos == int(local_field.pos)):
                            return member_parent
                return None

            pcap_layer_field_parent = None
            for member in family:
                pcap_layer_field_parent = find_pcap_layer_field_parent(member)
                if pcap_layer_field_parent is not None:
                    break

            if pcap_layer_field_parent is None:
                pcap_layer_field_parent = pcap_layer_field_root
            local_pcap_layer_field = PcapLayerField(local_field, pcap_layer_field_parent)
            node[int(local_field.pos)] = local_pcap_layer_field  # Update dictionary tree
            return local_pcap_layer_field

        field_insert = set()
        for field in layer._get_all_fields_with_alternates():
            field: LayerField
            field_unique_key: str = field.pos + '_' + field.name
            if field_unique_key in field_insert:
                return None
            pcap_layer_field = local_get_field_tree(field)
            if pcap_layer_field is not None:
                field_insert.add(field_unique_key)

        print(pcap_layer_field_root)
