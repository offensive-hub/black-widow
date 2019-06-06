# -*- coding: utf-8 -*-
"""
Python 3.5 Program to create music Database

Creato da Fabrizio Fubelli
"""

import os, codecs

from datetime import datetime
from tinytag import TinyTag
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from app.gui import MusicSort
from app.gui.modalities import Modality

# os.path.getsize(itempath)   PER DIMENSIONE FILE

class Database(Modality.Mod):
    def __init__(self):
        self.NAME = 'Fabri MusicDatabase'
        self.name = 'Database Musicale'
        self.id = 4
        self.UtilDict = {}
        self.Attr = ['FILE=', 'ALBUMARTIST=', 'DISC_NUMBER=', 'DISC_TOTAL=',
                    'ALBUM=', 'TRACK=', 'TITLE=', 'ARTIST=', 'DURATION=',
                    'BITRATE=', 'FILESIZE=', 'MODIFIED=']
        self.DetailedFiles = []
        self.DetailedFilesDir = ''
        self.old_dir = ''
        self.directory = ''
    # CALLED BY CONTROLLER
    def reset(self):
        self.Text.closefile()
        self.UtilDict = {}
        self.DetailedFiles = []
        self.DetailedFilesDir = ''
        self.Window.setWindowTitle(self.NAME)
    # INNER CLASS FUNCTIONS
    def __openDetailedFiles__(self):
        file = None
        if self.__rootCheck__():
            md = self.directory+'/MUSIC_SORT/DetailedFiles.np'
            if os.path.isfile(md):
                file = md
            else:
                alert = QMessageBox()
                alert.addButton(alert.Yes)
                alert.addButton(alert.No)
                alert.setDefaultButton(alert.No);
                alert.setWindowTitle('Errore')
                t1 = 'Il file "DetailedFiles.np" non risulta essere nella directory "MUSIC_SORT".\n'
                t2 = '''Se tale file non è stato spostato o rinominato dall'utente, si dovrebbe creare andando in modalità "Analisi e Creazione File per Database" e cliccando su "Crea lista dettagliata"'''
                alert.setInformativeText('Cercare manualmente il file "DetailedFiles.np" ?')
                alert.setText(t1+t2)
                if alert.exec_() == alert.Yes:
                    try:
                        file = QFileDialog.getOpenFileName(caption = 'Seleziona il file "DetailedFiles.np"')[0]
                    except Exception as e:
                        alert = QMessageBox()
                        alert.setWindowTitle('Errore')
                        alert.setText('Impossibile aprire il file:\n'+str(e))
                        alert.exec_()
                        return
                    if not file: return
                else: return
            try:
                with codecs.open(file, 'r', encoding='utf8') as mdr:
                    self.DetailedFiles = mdr.readlines()
                self.DetailedFilesDir = file
            except:
                self.__unableToOpenFile__(file)
    def __LineAttr__(self, line, key='', ind=1, u=5):
        try:
            next_attr = self.Attr[ind]
            len_next_attr = len(next_attr)
            new_u = u
            while line[new_u:new_u+len_next_attr] != next_attr:
                new_u += 1
            if ind == 1:
                key = line[u:new_u-3]
                self.UtilDict[key] = []
            else: self.UtilDict[key].append(line[u:new_u-3])
            self.__LineAttr__(line, key, ind+1, new_u+len_next_attr)
        except: # Arrivati all'ultimo attributo
            self.UtilDict[key].append(line[u:])
    def __createDatabaseDictionary__(self, file_list = None):
        if type(file_list) == str:
            try:
                with codecs.open(file_list, 'r', encoding='utf8') as mdr:
                    lines = mdr.readlines()
                    if len(lines) > 0: self.DetailedFiles = lines
                    else: return
                self.DetailedFilesDir = file_list
            except:
                self.__unableToOpenFile__(file_list)
                return
        elif len(self.DetailedFiles) == 0 or self.old_dir != self.directory:
            self.DetailedFiles = {}
            self.__openDetailedFiles__()
            if len(self.DetailedFiles) == 0: return
        self.old_dir = self.directory
        self.UtilDict = {}
        try:
            self.Window.setWindowTitle(self.NAME+' ('+self.DetailedFilesDir+')')
        except:
            None
        len_tot = len(self.DetailedFiles)-1
        for j in range(1, len(self.DetailedFiles)):
            line = self.DetailedFiles[j].strip()
            self.__LineAttr__(line)
            print('DIZIONARIO -> Creata voce '+str(j)+' / '+str(len_tot))
        if not file_list and self.__printRequest__():
            self.TextEdit.clear()
            for k in self.UtilDict.keys():
                self.TextEdit.append('\nKEY = '+k)
                i = 1
                for a in self.UtilDict[k]:
                    self.TextEdit.append(self.Attr[i]+'"'+str(a)+'"')
                    i+=1
    def __printRequest__(self):
        alert = QMessageBox()
        alert.addButton(alert.Yes)
        alert.addButton(alert.No)
        alert.setDefaultButton(alert.No);
        alert.setWindowTitle('Scegli')
        alert.setText('Si desidera stampare nel TextEditor il database?')
        if alert.exec_() == alert.Yes:
            return True
        else: return False
    def __startCallback__(self):
        self.__createDatabaseDictionary__()
    # PUBLIC FUNCTIONS
    def getDictionary(self, file):
        self.__createDatabaseDictionary__(file)
        return self.UtilDict
    # GRAPHIC
    def setMenu(self):
        self.Menu.clear()
        self.Text.defaultMenu(self.Menu, self.App)
        # menu Database
        database = self.Menu.addMenu('Database')
        self.Menu.addSeparator()
        apriDetailedFiles, ESEMPIO = self.__createSubActions__(database, ['Apri Lista Dettagliata (DA COMPILARE)', 'ESEMPIO'])
        self.Menu.setStyleSheet("color: white;"
                    "background-color: purple;"
                    "selection-color: purple;"
                    "selection-background-color: white;"
                    )
        self.Menu.adjustSize()
    def setWindow(self, Height):
        self.Window.setWindowTitle(self.NAME)
        window = QWidget()
        layout = QVBoxLayout() # ALL (UP and DOWN)
        buttonTEMP = QPushButton('START')
        buttonTEMP.clicked.connect(self.__startCallback__)

        layout.addWidget(buttonTEMP)
        layout.addWidget(self.SMbutton)
        layout.addWidget(self.TextEdit)

        window.setLayout(layout)
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("image/purple.jpg")))
        self.Window.setCentralWidget(window)
        self.Window.setPalette(palette)
    def setMod(self, win, textedit, height, menu, app, text, SMbutton):
        os.chdir(MusicSort.DIRECTORY)
        self.Text = text
        self.SMbutton = SMbutton
        self.Text.setActualName(self.NAME)
        self.Window = win
        self.Menu = menu
        self.TextEdit = textedit
        self.App = app
        self.setMenu()
        self.setWindow(height)
