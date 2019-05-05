"""
Gestione pcap
"""

from app.utils import settings
from app.utils.helpers.logger import Log
import pyshark, zlib

# @param filter https://wiki.wireshark.org/DisplayFilters
def sniff_pcap(filter=None, src_file=None, dest_file=None, interface=None, limit_length=None):
    def __pcap_callback__(pkt):
        if (limit_length != None and int(pkt.length) > limit_length):
            Log.info('Packet too long')
            return  # Il pacchetto è troppo lungo

        Log.info('Analyzing packet number '+str(pkt.number))
        Log.info('Layers: '+str(pkt.layers))
        #pkt.pretty_print()
        for layer in pkt.layers:
            if (layer.layer_name == 'data'):
                Log.success('DATA!')
                print(layer.tcp_reassembled_data)
                print('tcp_reassembled_length: '+str(layer.tcp_reassembled_length))
                print('tcp_segment: '+str(layer.tcp_segment))
                print('tcp_segment_count: '+str(layer.tcp_segment_count))
                print('tcp_segments: '+str(layer.tcp_segments))
            elif (layer.layer_name == 'ssl'):
                return
                layer.pretty_print()
                try:
                    Log.success('app_data')
                    print(layer.app_data)
                    print(layer.record)
                    print(layer.record_content_type)
                    print(layer.record_length)
                    print(layer.record_version)
                except AttributeError:
                    pass
        try:
            body = pkt.http.file_data
            print('\n\n----------------')
            #pkt.pretty_print()
            print('body: '+str(body))
            print(pkt.http.chat)                # Es. HTTP/1.1 200 OK\r\n
            print(pkt.http.chunk_boundary)      # Es. 0d:0a
            print(pkt.http.chunk_size)          # Es. 240
            print(pkt.http.content_encoding)    # Es. gzip
            print(pkt.http.content_type)        # Es. text/html; charset=UTF-8
            print(pkt.http.data)                # Es. ...
            print(pkt.http.data_data)           # Es. 1f:8b:08:...
            print(pkt.http.data_len)            # Es. 240
            print(pkt.http.date)                # Es. Thu, 04 Apr 2019 22:10:16 GMT
            print(pkt.http.file_data)           # Es. Some simple or decoded text...
            print(pkt.http.layer_name)          # Es. http
            print(pkt.http.prev_request_in)     # Es. 4973
            print(pkt.http.prev_response_in)    # Es. 4975
            print(pkt.http.request_in)          # Es. 5031
            print(pkt.http.response)            # Es. 1
            print(pkt.http.response_code)       # Es. 200
            print(pkt.http.response_code_desc)  # Es. OK
            print(pkt.http.response_for_uri)    # Es. http://fakesitecc19.altervista.org/
            print(pkt.http.response_line)       # Es. Date: Thu, 04 Apr 2019 22:10:16 GMT\xd\xa
            print(pkt.http.response_number)     # Es. 2
            print(pkt.http.response_phrase)     # Es. OK
            print(pkt.http.response_version)    # Es. HTTP/1.1
            print(pkt.http.server)              # Es. apache
            #print(pkt.http.time)
            #print(pkt.http.transfer_encoding)
            print('----------------\n\n')
        except Exception as e:
            Log.error(str(e))
            pass
            #Log.error(str(e))
            #print('\n\n')



        # 'captured_length', 'eth', 'frame_info', 'get_multiple_layers',
        # 'get_raw_packet', 'highest_layer', 'interface_captured', 'ip',
        # 'layers', 'length', 'number', 'pretty_print', 'show', 'sniff_time',
        # 'sniff_timestamp', 'ssl', 'dns', 'tcp', 'udp' 'transport_layer'
        #print('captured_length: '+str(pkt.captured_length))
        #print('frame_info: '+str(pkt.frame_info))
        #print('get_multiple_layers: '+str(pkt.get_multiple_layers('ssl')))
        #print('get_raw_packet: '+str(pkt.get_raw_packet()))    # use_json=True, include_raw=True # required in capture
        #print('highest_layer: '+str(pkt.highest_layer))
        #print('interface_captured: '+str(pkt.interface_captured))
        #print('layers: '+str(pkt.layers))
        #print('length: '+str(pkt.length))
        #print('number: '+str(pkt.number))
        #print('sniff_time: '+str(pkt.sniff_time))
        #print('sniff_timestamp: '+str(pkt.sniff_timestamp))
        #print('transport_layer: '+str(pkt.transport_layer))

    if (interface == None): interface = settings.Get.my_interface()
    if (src_file != None): capture = pyshark.FileCapture(src_file, display_filter=filter, output_file=dest_file)
    else: capture = pyshark.LiveCapture(interface, display_filter=filter, output_file=dest_file)
    capture.apply_on_packets(__pcap_callback__, timeout=None)
