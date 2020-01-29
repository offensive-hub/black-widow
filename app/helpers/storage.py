"""
*********************************************************************************
*                                                                               *
* storage.py -- Useful methods and classes to manage files and directory.       *
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

import os
import re
import shutil
import time

from .util import replace_regex


# @return true se il file contiene la stringa find, False altrimenti
def file_contains(find, file):
    # if APP_DEBUG: Log.info('CALLED: file_contains(' + find + ', ' + file + ')')
    if not os.path.isfile(file):
        return False
    with open(file) as f:
        s = f.read()
        return find in s


# @return string il contenuto del file
def read_file(file):
    # if APP_DEBUG: Log.info('CALLED: read_file(' + file + ')')
    if not os.path.isfile(file):
        return ""
    with open(file) as f:
        content = f.read()
        if type(content) == bytes:
            # noinspection PyUnresolvedReferences
            content = str(content.decode('utf-8'))
        return content.rstrip('\n')


# @return True se il file contiene l'espressione regolare regex, False altrimenti
def file_contains_regex(regex, file):
    # if APP_DEBUG: Log.info('CALLED: file_contains_regex(' + regex + ', ' + file + ')')
    if not os.path.isfile(file):
        return False
    reg = re.compile(regex)
    with open(file, 'r') as f:
        text = f.read()
    matches = re.findall(reg, text)
    return len(matches) > 0


def replace_in_file(find, replace, file):
    """
    Esegue il replace della stringa che trova, con la stringa nel parametro replace
    :param find: la stringa da trovare
    :param replace: la stringa che andra' a sostituire la stringa trovata
    :param file: il file in cui sovrascrivere find con replace
    :return: True se trova una stringa find, False altrimenti
    """
    # if APP_DEBUG:
    #    Log.info('CALLED: replace_in_file(' + find + ', ' + replace + ', ' + file + ')')
    if find == replace:
        return False
    if not file_contains(find, file):
        return False
    # Safely write the changed content, if found in the file
    with open(file, 'r') as f:
        t = f.read()
    with open(file, 'w') as f:
        s = t.replace(find, replace)
        f.write(s)
    return True


# Esegue il replace della regex che trova, con la stringa replace
# @param regex l'espressione regolare da trovare
# @param replace la stringa che andra' a sostituire la regex trovata
# @param file il file in cui sovrascrivere regex con replace
# @return True se trova una regex equivalente ad una stringa diversa da
#         replace, False altrimenti
def replace_in_file_regex(regex, replace, file):
    # if APP_DEBUG:
    #    Log.info('CALLED: replace_in_file_regex(' + regex + ', ' + replace + ', ' + file + ')')
    if not os.path.isfile(file):
        with open(file, 'a') as f:
            f.close()
    with open(file, 'r') as f:
        content = f.read()
    content_new = replace_regex(regex, replace, content)  # re.sub(regex, replace, content, flags = re.M)
    if content != content_new:
        overwrite_file(content_new, file)
        return True
    return False


# Sovrascrive il contenuto del file con content
def overwrite_file(content, file):
    # if APP_DEBUG:
    #    Log.info('CALLED: overwrite_file(' + content + ', ' + file + ')')
    with open(file, 'w') as f:
        f.write(str(content) + '\n')


# Appende content nel file
def append_in_file(content, file):
    with open(file, 'a') as f:
        f.write(str(content) + '\n')


# Se la cartella folder non esiste, la crea
def check_folder(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)


# Elimina tutti i files presenti nella cartella passata per argomento
def clean_folder(folder):
    # if APP_DEBUG:
    #    Log.info('CALLED: clean_folder(' + folder + ')')
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if file_path != folder:
                delete(file_path)
        return True
    return False


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


# Copia il file o la cartella "src", in "dest"
def copy(src, dest):
    # if APP_DEBUG:
    #    Log.info('CALLED: copy(' + src + ', ' + dest + ')')
    dest_parent = os.path.dirname(dest)
    check_folder(dest_parent)
    if os.path.exists(dest):
        delete(dest)
    if os.path.isdir(src):
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


# Muove il file o la cartella "src", in "dest"
def move(src, dest):
    # if (APP_DEBUG): Log.info('CALLED: move(' + src + ', ' + dest + ')')
    dest_parent = os.path.dirname(dest)
    check_folder(dest_parent)
    if os.path.exists(dest):
        delete(dest)
    shutil.move(src, dest)


def ls(directory: str) -> list:
    """
    Returns a list containing the names of the files in the directory.
    :param directory: The directory
    :return: The list of the files in the directory
    """
    return [os.path.join(directory, entry) for entry in os.listdir(directory)]


def basename(path: str) -> str:
    """
    Returns the final component of a pathname.
    :param path: The full path
    :return: the final component of a pathname
    """
    return os.path.basename(path)


def is_file(path: str) -> bool:
    """
    Test whether a path is a regular file.
    :param path: The file path
    :return: True if path is a file, otherwise False
    """
    return os.path.isfile(path)


# Elimina il file o la cartella passato per argomento
# noinspection PyBroadException
def delete(file):
    if file is None:
        return True
    attempts = 0
    while os.path.exists(file):
        try:
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.islink(file):
                os.unlink(file)
            elif os.path.isdir(file):
                shutil.rmtree(file)
        except PermissionError:
            return False
        except (Exception, IOError):
            attempts += 1
            if attempts >= 5:
                return False
            time.sleep(0.5)
    return True


def chmod(path, mode, recursive=False):
    os.chmod(path, mode)
    if not recursive:
        return
    for root, dirs, files in os.walk(path):
        for d in dirs:
            os.chmod(os.path.join(root, d), mode)
        for f in files:
            os.chmod(os.path.join(root, f), mode)
