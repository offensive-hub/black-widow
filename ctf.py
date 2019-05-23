#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File da cui eseguire gli script scritti per le ctf (cartella /ctf)
"""

import app, ctf, os
from app.utils.helpers.logger import Log

class Crypto:
    @staticmethod
    def block():
        my_list = range(0xfc60f4, 0xfe09b9)
        res = app.utils.helpers.multiprocess(target=ctf.crypto.block.block.main, args=(my_list,))
        print('Result: '+str(res))

def main():
    Log.info(app.env.APP_NAME+' (CTF) started, PID='+str(os.getpid()))
    Crypto.block()

if __name__ == "__main__":
    main()
