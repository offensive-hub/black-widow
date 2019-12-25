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

import codecs
import socket

import numpy
import pyshark

from app.utils import settings
from app.utils.helpers.util import replace_regex, regex_is_string
from app.utils.helpers.logger import Log

from . import MacManufacturer


def sniff_pcap(filters=None, src_file=None, dest_file=None, interface=None, limit_length=None, callback=None):
    """
    Packet capture method
    :param filters: https://wiki.wireshark.org/DisplayFilters
    :param src_file: Il file .pcap da cui leggere i pacchetti ascoltati (o None, per Live sniffing)
    :param dest_file: Il file in cui scrivere il .pcap dei pacchetti ascoltati (o None)
    :param interface: L'interfaccia da cui ascoltare (o None)
    :param limit_length: The limit length of each packet field (they will be truncated), or None
    :param callback: The callback method to call (or None)
    """

    mac_manufacturer = MacManufacturer()

    def __is_hash__(text: str) -> bool:
        return len(text) >= 8 and regex_is_string('^(([A-Z]|[a-z]|[0-9])+)+$', text)

    def __best_field__(original: str, decoded: str) -> str:
        if __is_hash__(original):
            return 'original'
        decoded = replace_regex('[^a-zA-Z0-9 \n\.]', '', decoded)
        if len(decoded) <= 5:
            return 'original'
        else:
            return 'decoded'

    def __pcap_callback__(pkt):
        # Log.info('Analyzing packet number ' + str(pkt.number))
        # Log.info('Layers: ' + str(pkt.layers))
        layers_dict = dict()
        pkt.pretty_print()  # Printa il pacchetto in modo comprensibile (non mostra importanti campi e non decodifica)
        for layer in pkt.layers:
            # for field_line in layer._get_all_field_lines():
            #     print(field_line)

            layer_fields = {}

            # Ripasso Layers:
            # Layers: ["2. Data Link (mac)",    "3. Network (ip)", "4. Transport (tcp/udp)", "5-6-7. *data"]
            # Layers: ["2. Collegamento (mac)", "3. Rete (ip)",    "4. Trasporto (tcp/udp)", "5-6-7. *dati"]

            if callback is None:
                print('Layer: ' + str(layer.layer_name))

            for field_name in numpy.unique(layer.field_names):
                layer_field_dict = {}

                dirty_field = layer.get_field(field_name).strip()

                if ('addr' in field_name or 'dst' in field_name or 'src' in field_name) and (':' in dirty_field):
                    field = dirty_field
                else:
                    try:
                        # Decodifico da esadecimale a utf-8 (se non è esadecimale, lancia eccezione)
                        field = bytes.fromhex(dirty_field.replace(":", " ")).decode('utf-8', 'ignore')
                    except ValueError or UnicodeDecodeError or TypeError:
                        # Decodifico in utf-8 (il doc non era in esadecimale)
                        field = codecs.decode(bytes(dirty_field, encoding='utf-8')).replace("\\r\\n", "")
                    # Ordino codice sostituendo caratteri di accapo e di tabulazione e pulisco la stringa
                    field = field \
                        .replace('\\xa', '\n') \
                        .replace('\\xd', '\n') \
                        .replace('\\x9', '\t') \
                        .replace('\\n', '\n') \
                        .strip()

                # salvo campi originale e decodificato
                layer_field_dict['decoded'] = field
                layer_field_dict['original'] = dirty_field

                if limit_length is not None:
                    # Verifico lunghezza campo decodificato
                    if len(field) > limit_length:
                        # Log.info('Truncated too long decoded field (old_length='+str(len(field))+',
                        # new_length='+str(limit_length)+')')
                        field = '[truncated]' + str(field[0:limit_length])
                        layer_field_dict['decoded_truncated'] = field

                    # Verifico lunghezza campo originale
                    if len(dirty_field) > limit_length:
                        # Log.info('Truncated too long original field (old_length='+str(len(dirty_field))+',
                        # new_length='+str(limit_length)+')')
                        dirty_field = '[truncated]' + str(dirty_field[0:limit_length])
                        layer_field_dict['original_truncated'] = dirty_field

                # Se il risultato della codifica è troppo corto, è probabilissimo che la decodifica
                # non abbia dato un valore sensato: consiglio di visualizzare il valore originale
                layer_field_dict['best'] = __best_field__(dirty_field, field)

                layer_fields[field_name] = layer_field_dict

                key = layer_field_dict['best']
                truncated_key = key + '_truncated'
                if truncated_key in layer_field_dict:
                    field = layer_field_dict[truncated_key]
                else:
                    field = layer_field_dict[key]

                # if (field_name == 'content_encoding'): content_encoding = field

                if callback is None:
                    print('   |--[ ' + str(field_name) + ' ] = ' + str(field))  # Printa stile albero

            layers_dict[layer.layer_name] = layer_fields

        # Creo un dizionario con le informazioni sul pacchetto catturato
        frame_info = dict()
        for field_name in pkt.frame_info.field_names:
            frame_info[field_name] = str(pkt.frame_info.get_field(field_name))
        pkt_dict = {
            'number': str(pkt.number),
            'captured_length': str(pkt.captured_length),
            'interface_captured': str(pkt.interface_captured),
            'highest_layer': str(pkt.highest_layer),
            'frame_info': frame_info,
            'length': str(pkt.length),
            'sniff_time': str(pkt.sniff_time),
            'sniff_timestamp': str(pkt.sniff_timestamp),
            'transport_layer': str(pkt.transport_layer),
            'layers': layers_dict  # Il dizionario dei livelli creato nel sovrastante loop
        }
        source = None
        destination = None
        source_host = 'Unknown'
        destination_host = 'Unknown'
        pkt_type = None
        pkt_dict_layers = pkt_dict.get('layers')
        # noinspection PyTypeChecker
        pkt_dict_ip: dict = pkt_dict_layers.get('ip')
        # noinspection PyTypeChecker
        pkt_dict_arp: dict = pkt_dict_layers.get('arp')
        # noinspection PyTypeChecker
        pkt_dict_eth: dict = pkt_dict_layers.get('eth')

        if pkt_dict_ip is not None:
            source = pkt_dict_ip['src']['decoded']
            destination = pkt_dict_ip['dst']['decoded']
        elif pkt_dict_arp is not None:
            source = pkt_dict_arp['src_proto_ipv4']['decoded']
            destination = pkt_dict_arp['dst_proto_ipv4']['decoded']
        elif pkt_dict_eth is not None:
            source = pkt_dict_eth['src']['decoded']
            destination = pkt_dict_eth['dst']['decoded']

        if source is not None:
            try:
                source_host = socket.gethostbyaddr(source)[0]
            except OSError:
                pass
        if destination is not None:
            try:
                destination_host = socket.gethostbyaddr(destination)[0]
            except OSError:
                pass

        pkt_dict['source'] = source
        pkt_dict['source_host'] = source_host
        pkt_dict['destination'] = destination
        pkt_dict['destination_host'] = destination_host

        transport_layer = pkt_dict.get('transport_layer')
        highest_layer = pkt_dict.get('highest_layer')
        if highest_layer != 'None':
            pkt_type = highest_layer
        elif transport_layer != 'None':
            pkt_type = transport_layer

        pkt_dict['type'] = pkt_type

        if callback is not None:
            callback(pkt_dict)

    if interface is None and src_file is None:
        interface = settings.Get.my_interface()
    if src_file is not None:
        Log.info('Analyzing file: ' + src_file)
        capture = pyshark.FileCapture(src_file, display_filter=filters, output_file=dest_file)
    else:
        Log.info('Analyzing live traffic')
        capture = pyshark.LiveCapture(interface, display_filter=filters, output_file=dest_file)
    capture.apply_on_packets(__pcap_callback__)
