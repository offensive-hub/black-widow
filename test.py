#!/usr/bin/env python3

"""
TEST MODULE
"""

import os, app
from termcolor import colored

def main():
    app.utils.helpers.logger.Log.info(app.env.APP_NAME+' (DEBUG) started, PID='+str(os.getpid()))
    if (not app.env.APP_DEBUG):
        print(colored("La modalità di APP_DEBUG non è attiva. Modificarla in 'app/env.py'.\n", 'red'))
        exit(1)
    Settings.main()
    #env()
    #log()
    #storage()
    exit(0)






class Settings:
    @staticmethod
    def main():
        print(colored("\nCHECK SETTINGS:", 'yellow'))
        Settings.imports()
        Settings.set()
        Settings.add()
        Settings.get()
        Settings.remove()

    @staticmethod
    def imports():
        print("app.utils.settings: " + str(dir(app.utils.settings)))
        print("app.utils.settings.Get: " + str(dir(app.utils.settings.Get)))
        print("app.utils.settings.Set: " + str(dir(app.utils.settings.Set)))

    @staticmethod
    def set():
        print("app.utils.settings.Set.my_ip()")
        print(str(app.utils.settings.Set.my_ip('127.0.0.1')))
        print("app.utils.settings.Set.game_server()")
        print(str(app.utils.settings.Set.game_server('192.168.1.1')))

    @staticmethod
    def get():
        print("app.utils.settings.Get.my_ip()")
        print(str(app.utils.settings.Get.my_ip()))
        print("app.utils.settings.Get.server_to_attack()")
        print(str(app.utils.settings.Get.server_to_attack()))
        print("app.utils.settings.Get.all()")
        print(str(app.utils.settings.Get.all()))

    @staticmethod
    def add():
        print("app.utils.settings.Add.server_to_attack()")
        print(str(app.utils.settings.Add.server_to_attack('8.8.8.8')))
        print(str(app.utils.settings.Add.server_to_attack('8.8.4.4')))
        print("app.utils.settings.Add.server_to_defend()")
        print(str(app.utils.settings.Add.server_to_defend('192.168.1.50')))
        print(str(app.utils.settings.Add.server_to_defend('192.168.1.51')))
        print("app.utils.settings.Add.team_player()")
        print(str(app.utils.settings.Add.team_player('192.168.1.155')))
        print(str(app.utils.settings.Add.team_player('192.168.1.78')))

    def remove():
        print("app.utils.settings.Remove.server_to_attack()")
        print(str(app.utils.settings.Remove.server_to_attack('8.8.8.8')))
        print("app.utils.settings.Remove.team_player()")
        print(str(app.utils.settings.Remove.team_player('192.168.1.78')))








def imports():
    # Check imports
    print(colored("\nCHECK IMPORTS:", 'yellow'))
    print("app: " + str(dir(app)))
    print("app.env: " + str(dir(app.env)))
    print("app.utils: " + str(dir(app.utils)))
    print("app.utils.helpers: " + str(dir(app.utils.helpers)))
    print("app.utils.helpers.logger: " + str(dir(app.utils.helpers.logger)))

def env():
    print(colored("\nCHECK ENVIRONMENTS:", 'yellow'))
    print("app.env.APP_DEBUG: " + str(app.env.APP_DEBUG))
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
