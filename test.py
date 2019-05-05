#!/usr/bin/env python3
"""
TEST MODULE
"""

import os, app
from termcolor import colored

def main():
    app.utils.helpers.logger.Log.info(app.env.APP_NAME+' (DEBUG) started, PID='+str(os.getpid()))
    if (not app.env.DEBUG):
        print(colored("La modalità di DEBUG non è attiva. Modificarla in 'app/env.py'.\n", 'red'))
        exit(1)
    imports()
    methods()
    env()
    json_settings()
    log()
    storage()
    exit(0)

def imports():
    # Check imports
    print(colored("\nCHECK IMPORTS:", 'yellow'))
    print("app: " + str(dir(app)))
    print("app.env: " + str(dir(app.env)))
    print("app.utils: " + str(dir(app.utils)))
    print("app.utils.util: " + str(dir(app.utils.util)))
    print("app.utils.helpers: " + str(dir(app.utils.helpers)))
    print("app.utils.helpers.logger: " + str(dir(app.utils.helpers.logger)))

def methods():
    print(colored("\nCHECK METHDOS:", 'yellow'))
    print("app.utils.util.pexec()")
    app.utils.util.pexec()

def env():
    print(colored("\nCHECK ENVIRONMENTS:", 'yellow'))
    print("app.env.DEBUG: " + str(app.env.DEBUG))
    print("app.env.APP_PATH: " + str(app.env.APP_PATH))
    print("app.env.APP_SETTINGS: " + str(app.env.APP_SETTINGS))

def json_settings():
    print(colored("\nCHECK JSON SETTINGS", 'yellow'))

def log():
    print(colored("\nCHECK LOG:", 'yellow'))
    print("dir(app.utils.helpers.logger.Log): " + str(dir(app.utils.helpers.logger.Log)))
    app.utils.helpers.logger.Log.info('PROVA INFO')
    app.utils.helpers.logger.Log.error('PROVA ERROR')
    app.utils.helpers.logger.Log.success('PROVA SUCCESS')

def storage():
    print(colored("\nCHECK STORAGE:", 'yellow'))
    print("dir(app.utils.helpers.storage): " + str(dir(app.utils.helpers.storage)))
    file1 = '/tmp/'+app.env.APP_PROC+'1'
    print(str(app.utils.helpers.storage.file_contains('STRING_TEST_1', file1)))
    print(str(app.utils.helpers.storage.read_file(file1)))
    print(str(app.utils.helpers.storage.file_contains_regex('STRING.*1', file1)))
    print(str(app.utils.helpers.storage.replace_in_file('STR_TO_FIND', 'NEW_STR', file1)))
    print(str(app.utils.helpers.storage.read_file(file1)))
    print(str(app.utils.helpers.storage.replace_in_file_regex('RE.+X_T._F.ND', 'NEW_STR', file1)))
    print(str(app.utils.helpers.storage.read_file(file1)))
    app.utils.helpers.storage.overwrite_file('NEW FILE CONTENT\nSTRING_TEST_1\nSTR_TO_FIND\nREGEX_TO_FIND', file1)
    file2 = '/tmp/'+app.env.APP_PROC+'2'
    app.utils.helpers.storage.append_in_file('CONTENT FOR FILE2', file2)
    file1_copy = '/tmp/'+app.env.APP_PROC+'1_copy'
    app.utils.helpers.storage.copy(file1, file1_copy)
    app.utils.helpers.storage.copy(app.env.APP_TMP, '/tmp/'+app.env.APP_PROC+'_copy')
    app.utils.helpers.storage.move('/tmp/'+app.env.APP_PROC+'_copy', '/tmp/'+app.env.APP_PROC+'_copy2')



main()
