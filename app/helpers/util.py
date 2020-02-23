"""
*********************************************************************************
*                                                                               *
* util.py -- Generic useful methods, used in all parts of software.             *
*                                                                               *
********************** IMPORTANT BLACK-WIDOW LICENSE TERMS **********************
*                                                                               *
* This file is part of black-widow.                                             *
*                                                                               *
* black-widow is free software: you can redistribute it and/or modify           *
* it under the terms of the GNU General Public License as published by          *
* the Free Software Foundation, either version 3 of the License, or             *
* (at your option) any later version.                                           *
*                                                                               *
* black-widow is distributed in the hope that it will be useful,                *
* but WITHOUT ANY WARRANTY; without even the implied warranty of                *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 *
* GNU General Public License for more details.                                  *
*                                                                               *
* You should have received a copy of the GNU General Public License             *
* along with black-widow.  If not, see <http://www.gnu.org/licenses/>.          *
*                                                                               *
*********************************************************************************
"""

import getpass
import random
import re
import os
import string
import subprocess

from datetime import datetime

from black_widow.app.env import IGNORE_NON_ROOT


def now() -> str:
    """
    :return: The current datetime as string
    """
    return str(datetime.now()).replace(' ', '_')


def timestamp() -> str:
    """
    :return: The current timestamp as string
    """
    return str(datetime.timestamp(datetime.now()))


def regex_in_string(regex, text) -> bool:
    """
    Checks if the input string contains the input regex
    :param regex: The regex to search
    :param text: The string to check
    :return: True if string contains regex, otherwise False
    """
    reg = re.compile(regex)
    matches = re.findall(reg, text)
    return len(matches) > 0


def regex_is_string(regex, text) -> bool:
    """
    Check if a string is equals to input regex
    :param regex: The regex to compare
    :param text: The string to compare
    :return: True, if the regex is equals to string
    """
    reg = re.compile(regex)
    return bool(reg.match(text))


def replace_regex(regex, replace, text) -> str:
    """
    Replace the regex in the string with another string
    :param regex: The regex to found
    :param replace: The replacer string
    :param text: The string where find and replace the regex
    :return: The input string with replaced regex
    """
    return re.sub(regex, replace, text, flags=re.M)


def is_listable(obj) -> bool:
    """
    Check if type(obj) is on of (list, tuple, dict, range)
    :param obj: An Object
    :return: True if obj is listable, otherwise False
    """
    return type(obj) in (list, tuple, dict, range)


def sort_dict(dictionary: dict) -> dict:
    """
    :param dictionary: The dictionary to sort
    :return: The sorted dictionary
    """
    sorted_dictionary = dict()
    i = 0
    for k in dictionary.keys():
        sorted_dictionary[i] = dictionary[k]
        i += 1
    return sorted_dictionary


def reverse_dict(dictionary: dict) -> dict:
    """
    :param dictionary: The dictionary to sort
    :return: The sorted dictionary
    """
    reversed_dictionary = dict()
    keys = list(dictionary.keys())
    keys.reverse()
    for k in keys:
        reversed_dictionary[k] = dictionary[k]
    return reversed_dictionary


def print_dict(dictionary: dict, depth: int = 0):
    """
    :type dictionary: dict
    :type depth: int
    """
    for key, value in dictionary.items():
        space = (' ' * depth) + '|-- '
        print(space + str(key) + ':')
        if type(value) is dict:
            print_dict(value, depth+1)
        else:
            print(space + ' [' + str(type(value)) + '] ' + str(value))


def rand_str(special: bool = True, length: int = 10) -> str:
    """
    Generates a random string
    :param special: True if you want to include special chars, otherwise False
    :param length: The generated string length
    :return: A random string
    """
    if length <= 1:
        return ''
    chars = string.ascii_letters + string.digits + string.punctuation
    if special:
        chars += string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


#################
# Process Utils #
#################

def pid_exists(pid: int) -> bool:
    """
    Checks if exists a process with input pid
    :param pid: The pid to check
    :return: True, if the pid exists, otherwise False
    """
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def is_executable(cmd_file: str) -> bool:
    """
    If cmd_file is a file this method checks if the current user can executes that,
    otherwise it checks if the current user can executes the associated file
    (returned by `type cmd_file`)
    :param cmd_file: The command or the file to executes
    :return: True, if the current user can executes "cmd_file", otherwise False
    """
    path = exec_type(cmd_file)
    return os.access(path, os.X_OK)


def is_root() -> bool:
    """
    If IGNORE_NON_ROOT in .env is False, this method checks if the current user is root
    :return: True, if the current user is root, otherwise False
    """
    if IGNORE_NON_ROOT:
        return True
    user = whoami(False)
    return user['uid'] == 0 or user['sudo']


def root_required():
    """
    If the current process has not root privileges, print the error and exits from app
    """
    if not is_root():
        print("\nThis feature requires root privileges!\n")
        exit(20)


def whoami(check_sudo: bool = True) -> dict:
    """
    Get the dictionary of current user info
    :param check_sudo: True, if you want get the user which executed sudo command
    :return: A dictionary with current user info
    """
    name = None
    uid = None
    gid = None
    sudo = True
    if check_sudo:
        name = os.environ.get('SUDO_USER')
        uid = os.environ.get('SUDO_UID')
        gid = os.environ.get('SUDO_GID')
    if name is None:
        sudo = False
        name = getpass.getuser()
        uid = os.getuid()
        gid = os.getgid()
    return {
        'name': str(name),
        'uid': int(uid),
        'gid': int(gid),
        'sudo': sudo
    }


def set_owner_process(user: dict):
    """ set user and group of workers processes """
    os.setgid(user['gid'])
    os.setuid(user['uid'])
    os.environ['USER'] = user['name']
    os.environ['LOGNAME'] = user['name']
    home_dirname = os.path.dirname(os.path.expanduser("~"))
    if home_dirname == '/' and user['sudo']:
        home_dirname = '/home'
    new_home = os.path.join(home_dirname, user['name'])
    os.environ['HOME'] = new_home


def os_exec(*args) -> list:
    """
    Executes through os stdin the input commands
    :param args: cmd + args (eg1. "cmd" "[args]"), (eg2. "ls" "-l")
    :return: The stdout of executed command
    """
    p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    list_stdout = []
    for line in p.stdout.readlines():
        list_stdout.append(str(line.decode('utf-8')).rstrip('\n'))
    return list_stdout


def exec_type(cmd: str) -> str or None:
    """
    Indicate how the input "cmd" would be interpreted if used as a command name.
    If "cmd" is a shell built-in or it does not exists, returns None
    :param cmd: The command to check
    :return: Usually, the interpreted path of input command
    """
    if type(cmd) is not str:
        raise ValueError("cmd must be a string")
    outputs = os_exec('type ' + cmd)
    if len(outputs) == 0:
        return None
    output: str = outputs[0]
    output_split = output.split(' ')
    cmd_file = output_split[-1]
    if os.path.isfile(cmd_file):
        return cmd_file
    return None
