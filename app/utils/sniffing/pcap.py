# -*- coding: utf-8 -*-

"""
*********************************************************************************
*                                                                               *
* pcap.py -- Packet Capture (pcap)                                              *
*                                                                               *
* Methods to sniff the network traffic through pyshark.                         *
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

# from pprint import pprint
from pyshark.packet.fields import LayerField, LayerFieldsContainer
from pyshark.packet.layer import Layer
from pyshark.packet.packet import Packet

# from app.env_local import APP_DEBUG
from app.utils import settings
from app.utils.helpers.util import replace_regex, regex_is_string, regex_in_string
from app.utils.helpers.logger import Log

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

        field_tree = dict()     # dict { pos => pkt }
        field_insert = dict()   # dict { key => pkt }
        max_depth = 6

        def local_get_field_tree(local_field: LayerField, local_parent: PcapLayerField = None):
            local_field_pos = int(local_field.pos)
            local_field_key = str(local_field_pos) + str(local_field.name)
            local_field_insert = field_insert.get(local_field_key)
            if local_field_insert is not None:
                return local_field_insert
            local_parent_real = field_tree.get(local_field_pos)
            if local_parent_real is not None:
                local_parent = local_parent_real
            if local_parent is not None:
                if local_parent.depth >= max_depth:
                    return None
            local_pcap_layer_field = PcapLayerField(local_field, local_parent)
            field_insert[local_field_key] = local_pcap_layer_field
            if local_parent is None:
                # The current local_field becomes a potential next parent
                field_tree[local_field_pos] = local_pcap_layer_field
            if isinstance(local_field, LayerFieldsContainer) and len(local_field.alternate_fields) > 0:
                for local_child_field in local_field.alternate_fields:
                    local_get_field_tree(local_child_field, local_pcap_layer_field)
                    # local_get_field_tree(local_child_field)
            return local_pcap_layer_field

        for field in layer._all_fields.values():
            field: LayerField
            pcap_layer_field = local_get_field_tree(field)
            #
            # pcap_layer_field_parent: PcapLayerField = field_tree.get(pcap_layer_field.pos)
            # if pcap_layer_field_parent is not None:
            #     pcap_layer_field_parent.children.app
            # field_parent_index = len(field_parent_queue) - 1
            # if field_parent_index >= 0:
            #     field_parent_dict = field_parent_queue[field_parent_index]
            #     field_parent = field_parent_dict.get('field')
            #     field_parent_size = field_parent_dict.get('size')
            #     # print('MAYBE I HAVE A PARENT:')
            #     # print(field_parent)
            #     # print('parent_curr_size = ' + str(field_parent_size))
            #     # print('ME:')
            #     # print(pcap_layer_field)
            #     # exit(0)
            #
            # if len(pcap_layer_field.children) > 0:
            #     field_parent_queue.append({
            #         'field': pcap_layer_field,
            #         'size': pcap_layer_field.size
            #     })
            if pcap_layer_field is not None:
                layer_dict['fields'].append(pcap_layer_field)

        for pos, pcap_layer_field in field_tree.items():
            print(pos)
            print(pcap_layer_field)

        # for pcap_layer_field in layer_dict.get('fields'):
        #     pcap_layer_field: PcapLayerField
        #     print(pcap_layer_field)

        return layer_dict

    @staticmethod
    def _get_field_tree(field: LayerField, parent: PcapLayerField = None):
        pcap_layer_field = PcapLayerField(field, parent)
        if isinstance(field, LayerFieldsContainer) and len(field.alternate_fields) > 0:
            for child_field in field.alternate_fields:
                Pcap._get_field_tree(child_field, pcap_layer_field)
        return pcap_layer_field


    # noinspection PyProtectedMember
    @staticmethod
    def _get_layer_dict_old(layer: Layer) -> dict:
        """
        :param layer: The layer to process
        :return: The dictionary of layer
        """
        layer_dict = {
            'name': layer.layer_name,
            'fields': []
        }

        # for key, field in layer._all_fields.items():
        #     print(str(key) + ' => ' + str(field))
        #     if isinstance(layer, LayerFieldsContainer):
        #         children = []
        #         for field_layer.all_fields
        #     else:
        #         children = None
        #     pcap_layer_field = PcapLayerField(field)

        # layer_dict['fields'].append(pcap_layer_field)

        for pcap_layer_field in layer_dict.get('fields'):
            pcap_layer_field: PcapLayerField
            print(pcap_layer_field)

        exit(0)

        parent_field_index = -1
        parent_field_length = -1
        tag_field_index = -1
        tag_field_child_index = -1
        tag_field_size = 0
        for field in layer._all_fields.values():
            field: LayerField or LayerFieldsContainer
            if len(field.all_fields) > 1:
                print(field.all_fields)
                exit(0)
            field_dict = Pcap._get_field_dict(field)
            field_dict.update({
                'key': layer._sanitize_field_name(field.name),
                'children': []
            })
            field_name: str = field_dict.get('name')
            is_tag = 'Tagged parameters (' in field_dict.get('value')
            if field_name is None:
                field_dict['label'] = field_dict.get('value')
                field_dict['value'] = None
            if is_tag:
                # Start tag
                tag_field_index = len(layer_dict['fields'])
                tag_field_size = field_dict.get('size')
            is_child = False
            if field_name is not None:
                equal_index = field_name.find(' = ')
                binary_key = field_name[0:equal_index]
                if equal_index >= 0 and regex_in_string('^(\.| |0|1)+$', binary_key):
                    if parent_field_index == -1:
                        parent_field_index = len(layer_dict['fields']) - 1
                        parent_field_length = len(binary_key)
                        is_child = True
                    elif len(binary_key) != parent_field_length:
                        is_child = False
                    else:
                        is_child = True
                    if is_child:
                        layer_dict['fields'][parent_field_index]['children'].append(field_dict)
            is_tag_child = not (is_child or is_tag) and tag_field_size > 0
            is_tag_child = False
            if is_tag_child:
                tag_field: dict = layer_dict['fields'][tag_field_index]
                if tag_field.get('size') == tag_field_size:
                    is_tag_child = False
                    if field_name == 'Tag':
                        tag_field['tag'] = field_dict
                    elif field_name == 'Tag Number':
                        tag_field['tag_number'] = field_dict
                    elif field_name == 'Tag length':
                        tag_field['tag_length'] = field_dict
                    else:
                        # First tag
                        is_tag_child = True
                        tag_field_child_index = -1
                if is_tag_child:
                    tag_field_tags: dict = tag_field.get('tag')
                    tag_field_numbers: dict = tag_field.get('tag_number')
                    tag_field_lengths: dict = tag_field.get('tag_length')
                    tag_field_size -= field_dict.get('size')
                    tag_field_child_index += 1
                    if tag_field_child_index == 0:
                        field_dict['label'] = 'Tag: ' + tag_field_tags.get('value')
                        field_dict['children'].append({
                            'name': 'Tag Number',
                            'value': tag_field_numbers.get('value')
                        })
                        field_dict['children'].append({
                            'name': 'Tag length',
                            'value': tag_field_lengths.get('value')
                        })
                    else:
                        if tag_field_child_index >= len(tag_field_tags.get('alternate_values')):
                            print(field_dict)
                            exit(0)
                            break
                        field_dict['label'] = 'Tag: ' + tag_field_tags.get('alternate_values')[tag_field_child_index]
                        field_dict['children'].append({
                            'name': 'Tag Number',
                            'value': tag_field_numbers.get('alternate_values')[tag_field_child_index]
                        })
                        field_dict['children'].append({
                            'name': 'Tag length',
                            'value': tag_field_lengths.get('alternate_values')[tag_field_child_index]
                        })
                    field_dict['children'].append({
                        'name': field_dict.get('name'),
                        'value': field_dict.get('value')
                    })
                    field_dict['value'] = None
                    tag_field['children'].append(field_dict)

            elif not is_child:
                parent_field_index = -1
                layer_dict['fields'].append(field_dict)
        return layer_dict

    @staticmethod
    def _get_field_dict(field: LayerField) -> dict:
        """
        :param field: The field to process
        :return: The dictionary of field
        """
        value = Pcap._get_field_value(field)
        field_dict = {
            'name': Pcap._get_field_label(field),
            'value':  value,
            'size': float(field.size),
            'pos': int(field.pos),
            'alternate_values': []
        }
        if isinstance(field, LayerFieldsContainer) and len(field.alternate_fields) > 0:
            for field_alternate in field.alternate_fields:
                field_dict['alternate_values'].append(Pcap._get_field_value(field_alternate))
        return field_dict

    @staticmethod
    def _get_field_label(field: LayerField) -> str or None:
        field_name: str = field.showname_key
        if not field_name:
            return None
        return field_name

    @staticmethod
    def _get_field_value(field: LayerField) -> str:
        field_value: str = field.showname_value
        if not field_value:
            field_value = field.get_default_value()
        if field_value is not None:
            field_value = field_value.encode('utf-8').decode('unicode-escape').replace('Âµs', 'µs')
        return field_value

    @staticmethod
    def _is_hash(text: str) -> bool:
        return len(text) >= 8 and regex_is_string('^(([A-Z]|[a-z]|[0-9])+)+$', text)

    @staticmethod
    def _best_field(original: str, decoded: str) -> str:
        if Pcap._is_hash(original):
            return 'original'
        decoded = replace_regex('[^a-zA-Z0-9 \n\.]', '', decoded)
        if len(decoded) <= 5:
            return 'original'
        else:
            return 'decoded'
