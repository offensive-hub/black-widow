# -*- coding: utf-8 -*-

"""
Packet Capture (pcap)
"""

from app.env import APP_DEBUG
from app.utils import settings
from app.utils.helpers.util import replace_regex, regex_in_string
from app.utils.helpers.logger import Log
import pyshark, zlib, numpy, codecs

# @param filter https://wiki.wireshark.org/DisplayFilters
def sniff_pcap(filter=None, src_file=None, dest_file=None, interface=None, limit_length=None):
    def __pcap_callback__(pkt):
        Log.info('Analyzing packet number '+str(pkt.number))
        Log.info('Layers: '+str(pkt.layers))
        #pkt.pretty_print()
        for layer in pkt.layers:
            print('Layer: '+str(layer.layer_name))
            for field_name in numpy.unique(layer.field_names):
                dirty_field = layer.get_field(field_name).rstrip()
                try:
                    field = bytes.fromhex(dirty_field.replace(":", "")).decode('utf-8')
                except ValueError or UnicodeDecodeError or TypeError as e:
                    field = codecs.decode(bytes(dirty_field, encoding='utf-8')).replace("\\r\\n", "")
                field = field.replace('\\xa', '\n')
                field = field.replace('\\x9', '\t')
                if (len(field) > limit_length):
                    Log.info('Truncated too long field (old_length='+str(len(field))+', new_length='+str(limit_length)+')')
                    field = '[truncated]' + str(field[0:limit_length])
                print('   |-- Field: '+str(field_name)+' -> '+str(field))
    if (interface == None): interface = settings.Get.my_interface()
    if (src_file != None): capture = pyshark.FileCapture(src_file, display_filter=filter, output_file=dest_file)
    else: capture = pyshark.LiveCapture(interface, display_filter=filter, output_file=dest_file)
    capture.apply_on_packets(__pcap_callback__, timeout=None)
