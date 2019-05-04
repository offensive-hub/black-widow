#!/usr/bin/env python3

import app

def main_debug():
    if (not app.env.DEBUG):
        print("La modalità di DEBUG non è attiva. Modificarla in 'app/env.py'.")
        exit(1)
    start()
    exit(0)

def start():
    imports()
    methods()

def imports():
    # Check imports
    print("app: " + str(dir(app)))
    print("app.env: " + str(dir(app.env)))
    print("app.utils: " + str(dir(app.utils)))
    print("app.utils.util: " + str(dir(app.utils.util)))

def methods():
    print("app.utils.util.pexec()")
    app.utils.util.pexec()

main_debug()
