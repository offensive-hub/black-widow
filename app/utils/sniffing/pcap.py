"""
Gestione pcap
"""

from app.utils import settings
import pyshark

def __manage_capture__(capture):
    def __pcap_callback__(pkt):
        print('\n\n\n\n\n\n')
        # 'captured_length', 'eth', 'frame_info', 'get_multiple_layers',
        # 'get_raw_packet', 'highest_layer', 'interface_captured', 'ip',
        # 'layers', 'length', 'number', 'pretty_print', 'show', 'sniff_time',
        # 'sniff_timestamp', 'ssl', 'dns', 'tcp', 'udp' 'transport_layer'
        pkt.pretty_print()
        #print('captured_length: '+str(pkt.captured_length))
        #print('frame_info: '+str(pkt.frame_info))
        #print('get_multiple_layers: '+str(pkt.get_multiple_layers('ssl')))
        #print('get_raw_packet: '+str(pkt.get_raw_packet()))    # use_json=True, include_raw=True # required in capture
        #print('highest_layer: '+str(pkt.highest_layer))
        #print('interface_captured: '+str(pkt.interface_captured))
        #print('layers: '+str(pkt.layers))
        for layer in pkt.layers:
            pass
            #print('layer: '+str(layer))
        #print('length: '+str(pkt.length))
        #print('number: '+str(pkt.number))
        #print('sniff_time: '+str(pkt.sniff_time))
        #print('sniff_timestamp: '+str(pkt.sniff_timestamp))
        #print('transport_layer: '+str(pkt.transport_layer))
    capture.apply_on_packets(__pcap_callback__, timeout=None)

# @param filter https://wiki.wireshark.org/DisplayFilters
#               tcp.port eq 53 or udp.port eq 53
def sniff_pcap(filter=None, src_file=None, dest_file=None, interface=None):
    if (interface == None): interface = settings.Get.my_interface()
    if (src_file != None): capture = pyshark.FileCapture(src_file, display_filter=filter)
    else: capture = pyshark.LiveCapture(interface, display_filter=filter)
    __manage_capture__(capture)
