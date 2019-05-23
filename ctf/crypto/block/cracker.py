#!/usr/bin/env python3

import sys
from block import encrypt_data, decrypt_data
plain_text = 'message: '
cipher_text = open('encrypted').read(len(plain_text))

data = {}
for i in range(0, 16**6):
    data[encrypt_data(plain_text, i)] = i

for i in range(0, 16**6):
    c = decrypt_data(cipher_text, i)
    if c in data:
        print '{0:x} {1:x}'.format(data[c], i)
