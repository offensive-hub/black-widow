# -*- coding: utf-8 -*-

"""
Packet Capture (pcap)
"""

from app.env import APP_DEBUG
from app.utils import settings
from app.utils.helpers.util import replace_regex, regex_in_string
from app.utils.helpers.logger import Log
import pyshark, numpy, codecs

# @param filter https://wiki.wireshark.org/DisplayFilters
# @param src_file Il file .pcap da cui leggere i pacchett ascoltati (o None, per Live sniffing)
# @param dest_file Il file in cui scrivere il .pcap dei pacchetti ascoltati (o None)
# @param interface L'interfaccia da cui ascoltare (o None)
# @param limit_length Il limite che i campi dei pacchetti devono avere per non essere troncati (o None)
# @param callback La funzione che prende un dizionario del pacchetto come argomento (o None)
# @return void
def sniff_pcap(filter=None, src_file=None, dest_file=None, interface=None, limit_length=None, callback=None):
    def __pcap_callback__(pkt):
        Log.info('Analyzing packet number '+str(pkt.number))
        Log.info('Layers: '+str(pkt.layers))
        layers_dict = {}
        #pkt.pretty_print()     # Printa il pacchetto in modo comprensibile (non mostra importanti campi e non decodifica nulla)
        for layer in pkt.layers:
            layer_fields = {}

            # Ripasso Layers:
            # Layers: ["2. Data Link (mac)",    "3. Network (ip)", "4. Transport (tcp/udp)", "5-6-7. *data"]
            # Layers: ["2. Collegamento (mac)", "3. Rete (ip)",    "4. Trasporto (tcp/udp)", "5-6-7. *dati"]

            #print('Layer: '+str(layer.layer_name))     # Decommentare per printare stile albero

            for field_name in numpy.unique(layer.field_names):
                layer_field_dict = {}

                dirty_field = layer.get_field(field_name).rstrip()

                try:
                    # Decodifico da esadecimale a utf-8 (se non è esadecimale, lancia eccezione)
                    field = bytes.fromhex(dirty_field.replace(":", " ")).decode('utf-8', 'ignore')
                except ValueError or UnicodeDecodeError or TypeError as e:
                    # Decodifico in utf-8 (il doc non era in esadecimale)
                    field = codecs.decode(bytes(dirty_field, encoding='utf-8')).replace("\\r\\n", "")
                # Ordino codice sostituendo caratteri di accapo e di tabulazione e pulisco la stringa
                field = field.replace('\\xa', '\n').replace('\\xd', '\n').replace('\\x9', '\t').replace('\\n', '\n').rstrip()

                # salvo campi originale e decodificato
                layer_field_dict['decoded'] = field
                layer_field_dict['original'] = dirty_field

                # Verifico lunghezza campo decodificato
                if (len(field) > limit_length):
                    #Log.info('Truncated too long decoded field (old_length='+str(len(field))+', new_length='+str(limit_length)+')')
                    field = '[truncated]' + str(field[0:limit_length])
                    layer_field_dict['decoded_truncated'] = field

                # Verifico lunghezza campo originale
                if (len(dirty_field) > limit_length):
                    #Log.info('Truncated too long original field (old_length='+str(len(dirty_field))+', new_length='+str(limit_length)+')')
                    dirty_field = '[truncated]' + str(dirty_field[0:limit_length])
                    layer_field_dict['original_truncated'] = dirty_field

                # Se il risultato della codifica è troppo corto, è probabilissimo che la decodifica
                # non abbia dato un valore sensato: consiglio di visualizzare il valore originale
                if (len(field) <= 5): layer_field_dict['best'] = 'original'
                else: layer_field_dict['best'] = 'decoded'

                #print('   |-- Field (original): '+str(field_name)+' -> '+str(dirty_field)) # Decommentare per printare stile albero
                #print('   |-- Field (decoded):  '+str(field_name)+' -> '+str(field))       # Decommentare per printare stile albero

                layer_fields[field_name] = layer_field_dict

            layers_dict[layer.layer_name] = layer_fields

        # Creo un dizionario con le informazioni sul pacchetto catturato
        pkt_dict = {
            'number': pkt.number,
            'captured_length': pkt.captured_length,
            'interface_captured': pkt.interface_captured,
            'highest_layer': pkt.highest_layer,
            'frame_info': pkt.frame_info,
            'length': pkt.length,
            'sniff_time': pkt.sniff_time,
            'sniff_timestamp': pkt.sniff_timestamp,
            'transport_layer': pkt.transport_layer,
            'layers': layers_dict   # Il dizionario dei livelli creato nel sovrastante loop
        }

        if (callback != None): callback(pkt_dict)   # chiamo la callback

    if (interface == None): interface = settings.Get.my_interface()
    if (src_file != None): capture = pyshark.FileCapture(src_file, display_filter=filter, output_file=dest_file)
    else: capture = pyshark.LiveCapture(interface, display_filter=filter, output_file=dest_file)
    capture.apply_on_packets(__pcap_callback__, timeout=None)
