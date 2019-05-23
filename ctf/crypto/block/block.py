#!/usr/bin/env python3
from sys import argv, exit
import struct, codecs
from os.path import isfile

SBoxes = [[15, 1, 7, 0, 9, 6, 2, 14, 11, 8, 5, 3, 12, 13, 4, 10], [3, 7, 8, 9, 11, 0, 15, 13, 4, 1, 10, 2, 14, 6, 12, 5], [4, 12, 9, 8, 5, 13, 11, 7, 6, 3, 10, 14, 15, 1, 2, 0], [2, 4, 10, 5, 7, 13, 1, 15, 0, 11, 3, 12, 14, 9, 8, 6], [3, 8, 0, 2, 13, 14, 5, 11, 9, 1, 7, 12, 4, 6, 10, 15], [14, 12, 7, 0, 11, 4, 13, 15, 10, 3, 8, 9, 2, 6, 1, 5]]

SInvBoxes = [[3, 1, 6, 11, 14, 10, 5, 2, 9, 4, 15, 8, 12, 13, 7, 0], [5, 9, 11, 0, 8, 15, 13, 1, 2, 3, 10, 4, 14, 7, 12, 6], [15, 13, 14, 9, 0, 4, 8, 7, 3, 2, 10, 6, 1, 5, 11, 12], [8, 6, 0, 10, 1, 3, 15, 4, 14, 13, 2, 9, 11, 5, 12, 7], [2, 9, 3, 0, 12, 6, 13, 10, 1, 8, 14, 7, 11, 4, 5, 15], [3, 14, 12, 9, 5, 15, 13, 2, 10, 11, 8, 4, 1, 6, 0, 7]]

def S(block, SBoxes):
    output = 0
    for i in range(0, len(SBoxes)):
        output |= SBoxes[i][(block >> 4*i) & 0b1111] << 4*i
    return output


PBox = [13, 3, 15, 23, 6, 5, 22, 21, 19, 1, 18, 17, 20, 10, 7, 8, 12, 2, 16, 9, 14, 0, 11, 4]
PInvBox = [21, 9, 17, 1, 23, 5, 4, 14, 15, 19, 13, 22, 16, 0, 20, 2, 18, 11, 10, 8, 12, 7, 6, 3]
def permute(block, pbox):
    output = 0
    for i in range(24):
        bit = (block >> pbox[i]) & 1
        output |= (bit << i)
    return output

def encrypt_data(data, key):
    enc = ""
    for i in range(0, len(data), 3):
        hex_block = codecs.encode(data[i:i+3].encode(), encoding='hex')
        block = int(hex_block, 16)
        #block = int(data[i:i+3].encode('hex'), 16)

        for j in range(0, 3):
            block ^= key
            block = S(block, SBoxes)
            block = permute(block, PBox)

        block ^= key
        hex_block = codecs.decode(("%06x" % block).encode(), encoding='hex').decode('latin-1')
        enc += hex_block
        #enc += ("%06x" % block).decode('hex')

    return enc

def decrypt_data(data, key):
    dec = ""
    for i in range(0, len(data), 3):
        hex_block = codecs.encode(data[i:i+3].encode(), encoding='hex')
        block = int(hex_block, 16)
        #block = int(data[i:i+3].encode('hex'), 16)

        block ^= key
        for j in range(0, 3):
            block = permute(block, PInvBox)
            block = S(block, SInvBoxes)
            block ^= key
        hex_block = codecs.decode(("%06x" % block).encode(), encoding='hex').decode('latin-1')
        dec += hex_block
        #dec += ("%06x" % block).decode('hex')

    return dec

def encrypt(data, key1, key2):
    encrypted = encrypt_data(data, key1)
    # 1st layer:   45 11 d9 8a 37 41 53 f8 1e fb 53 45
    # 2nd layer:   e5 16 da dc 93 07 fe 15 f0 1f 0d 1b
    # data:        m  e  s  s  a  g  e  :     a  a  \n
    encrypted = encrypt_data(encrypted, key2)
    return encrypted

def decrypt(data, key1, key2):
    decrypted = decrypt_data(data, key2)
    decrypted = decrypt_data(decrypted, key1)
    return decrypted

def usage():
    print("Usage: %s [encrypt/decrypt] [key1] [key2] [in_file] [out_file]" % argv[0])
    exit(1)

def main(my_list):
    keys1 = {}
    for i in my_list:
        header1 = codecs.encode(encrypt_data('message: aaa', i).encode(), encoding='hex').decode('latin-1')[0:18]
        #header1 = encrypt_data('message: aaa', i).encode("hex")[0:18]
        keys1[header1] = i
        if (i % 10000 == 0): print(header1+': 0x%06x' % i)
    print("len(keys1):", len(keys1))
    in_file = open("encrypted", "r", encoding='latin-1')
    data = ""
    while True:
        read = in_file.read(1024)
        if len(read) == 0:
            break
        data += read
    in_file.close()
    for i in my_list:
        header1 = codecs.encode(decrypt_data(data, i).encode(), encoding='hex').decode('latin-1')[0:18]
        #header1 = decrypt_data(data, i).encode("hex")[0:18]
        if (i % 10000 == 0):
            print(header1+': 0x%06x' % i)
        if header1 in keys1:
            print('Solved! key1: 0x%06x key2: 0x%06x' % (keys1[header1], i))
            return {
                'key1': str('0x%06x' % keys1[header1]),
                'key2': str('0x%06x' % i)
            }
