#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interfaccia grafica
"""

import os
import codecs
import sys
from .modalities import Search, Sorting, EditByFile, Database

from datetime import datetime
from tinytag import TinyTag
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


# DIRECTORY
DIRECTORY = os.getcwd()


############################## CLASSE PRINCIPALE ###############################
class Controller:
    def __init__(self):
        self.name = 'Controller'
        self.Width = None
        self.Height = None
        self.textedit = None
        self.CB_edit = None
        self.copy_FLAC = None
        self.menu_cFLAC = None
        self.move_FLAC = None
        self.menu_mFLAC = None
        self.WIN = None
        self.opened_file = ''
        self.APP = None
        self.MENU = None
        self.buttonSorted_Music = None
        # MODALITA' (e Menu)
        self.menuSORTING = None
        self.menuSEARCH = None
        self.menuTEXT = None
        self.ACTUAL_MOD = None
        self.Text = TextEditorMod()
        self.Menus = []
        self.Sorted_Music = ''
    def init(self):
        '''Crea un'applicazione Qt e una finestra'''
        app = QApplication.instance()
        if not app: # verifica se già esiste l'applicazione, o ne crea una nuova
            app = QApplication([])
        app.setWindowIcon(QIcon('image/icon.ico'))
        V = app.desktop().screenGeometry()
        self.Height = V.height()
        self.Width = V.width()
        return app
    def run(self, app):
        '''Rende la finestra visibile e lancia l'applicazione'''
        #window.showFullScreen()
        self.WIN.showMaximized()
        app.exec_()
    def textMod(self):
        self.modGeneric(0)
    def sortingMod(self):
        self.modGeneric(1)
    def searchMod(self):
        self.modGeneric(2)
    def modByFileMod(self):
        self.modGeneric(3)
    def modDatabase(self):
        self.modGeneric(4)
    def modGeneric(self, identifier):
        self.Menus[identifier].setChecked(True)
        if self.ACTUAL_MOD:
            if self.ACTUAL_MOD.id != identifier:
                self.ACTUAL_MOD.reset()
        self.ACTUAL_MOD = eval(self.ModForEval[identifier])
        self.buttonSorted_Music = QPushButton('Sorted_Music')
        self.buttonSorted_Music.clicked.connect(self.select_Sorted_Music)
        self.uncheckMenus(identifier)
    def uncheckMenus(self, i):
        self.textedit.setMaximumSize(self.tSize)
        self.ACTUAL_MOD.setMod(self.WIN, self.textedit, self.Height, self.MENU, self.APP, self.Text, self.buttonSorted_Music)
        for j in range(len(self.Menus)):
            if j != i: self.Menus[j].setChecked(False)
        self.addModalitiesMenu(self.MENU)
        self.ACTUAL_MOD.directory = self.Sorted_Music
        if self.Sorted_Music: os.chdir(self.Sorted_Music)
    def select_Sorted_Music(self):
        newdir = str(QFileDialog.getExistingDirectory(caption = 'Selezionare la directory "Sorted_Music"'))
        if newdir:
            self.Sorted_Music=newdir
            if self.textedit: self.textedit.clear()
            self.ACTUAL_MOD.directory = self.Sorted_Music
            os.chdir(self.Sorted_Music)
            self.textedit.append("Directory principale selezionata:\n"+self.Sorted_Music)
            if self.ACTUAL_MOD and self.ACTUAL_MOD.id == 1:
                if self.ACTUAL_MOD.AZ:
                    self.textedit.append("\nDirectory secondaria:\n"+self.ACTUAL_MOD.AZ)
    def addModalitiesMenu(self, menu):
        '''chiamato dal controllore. Aggiorna le modalità nel menu'''
        #if not menu: menu = self.MENU
        mod = menu.addMenu('&Modalità')
        self.menuTEXT = mod.addAction('Editor di Testo')
        self.menuSORTING = mod.addAction('Ordinamento Musica')
        self.menuMOD_BY_FILE = mod.addAction('Analisi e Creazione File per Database')
        self.menuSEARCH = mod.addAction('Ricerca Musica')
        self.menuDATABASE = mod.addAction('Database Musicale')
        self.Menus = [self.menuTEXT, self.menuSORTING, self.menuSEARCH, self.menuMOD_BY_FILE, self.menuDATABASE]
        self.Modalities = [self.textMod, self.sortingMod, self.searchMod, self.modByFileMod, self.modDatabase]
        self.ModForEval = ['self.Text', 'Sorting.SortingMod()', 'Search.SearchMod()', 'EditByFile.EditByFileMod()', 'Database.Database()']
        for i in range(len(self.Menus)):
             self.Menus[i].triggered.connect(self.Modalities[i])
             self.Menus[i].setCheckable(True)
        if self.ACTUAL_MOD:
            self.Menus[self.ACTUAL_MOD.id].setChecked(True)
    def createMenu(self, app = None):
        if not app: app = self.APP
        main_window = QMainWindow()
        m = main_window.menuBar()
        main_window.setWindowIcon(QIcon('image/icon.ico'))
        self.addModalitiesMenu(m)
        return main_window, m
    def main(self):
        self.APP = self.init()
        self.textedit = QTextEdit('')
        self.textedit.setLineWrapMode(self.textedit.NoWrap)
        self.tSize = self.textedit.maximumSize()
        self.WIN, self.MENU = self.createMenu()
        self.textMod()
        self.run(self.APP)


################################ TEXT EDITOR ##################################

class TextEditorMod:
    def __init__(self):
        self.id = 0
        self.NAME = 'Fabri TextEditor'
        self.name = 'Modalità Editor di Testo'
        self.opened_file = ''
        self.directory = ''
    def reset(self):
        self.closefile()
    def setWindow(self, Height):
        self.Window.setWindowTitle(self.NAME)
        window = QWidget()
        signature = QLabel()
        signature.setText('Editor di Testo di Fabrizio')
        signature.setTextFormat(Qt.TextFormat(3))
        signature.setStyleSheet("color: orange")
        layout = QVBoxLayout() # ALL (UP and DOWN)
        layout.addWidget(signature)
        signature.setAlignment(Qt.AlignRight)
        layout.addWidget(self.TextEdit)

        dist = Height/50
        layout.setContentsMargins(dist, dist, dist, dist)
        window.setLayout(layout)

        window.setLayout(layout)
        self.Window.setCentralWidget(window)
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("image/colors.jpg")))
        self.Window.setPalette(palette)

    def setMenu(self):
        self.Menu.clear()
        self.Menu.setStyleSheet("color: black;")
        self.defaultMenu(self.Menu, self.App)
        self.Menu.adjustSize()
    def setMod(self, win, textedit, height, menu, app, text, SMbutton):
        os.chdir(DIRECTORY)
        self.Window = win
        self.TextEdit = textedit
        self.App = app
        self.Menu = menu
        self.setMenu()
        self.setWindow(height)

        self.ActualName = 'Fabri TextEditor'
    def openfile(self):
        try:
            file = QFileDialog.getOpenFileName()[0]
        except:
            None
        if not file: return
        self.TextEdit.clear()
        try:
            with codecs.open(file, 'r', encoding='utf8') as f:
                self.TextEdit.append(f.read())
            self.Window.setWindowTitle(self.ActualName+' ('+file+')')
            self.opened_file = file
        except Exception as e:
            self.TextEdit.append('Impossibile aprire il file selezionato.')
            self.TextEdit.append('Eccezione:   '+str(e))
    def save(self):
        if not self.opened_file:
            self.savewithname()
            return
        text = ''
        if self.opened_file[-5:] == '.html' or self.opened_file[-4:] == 'htm':
            text = self.TextEdit.document().toHtml()
        else: text = self.TextEdit.toPlainText()
        try:
            with codecs.open(self.opened_file, 'w', encoding='utf8') as f:
                f.write(text)
        except Exception as e:
            self.TextEdit.append('Impossibile salvare.')
            self.TextEdit.append('Eccezione:   '+str(e))
    def savewithname(self):
        try:
            file = QFileDialog.getSaveFileName()[0]
        except:
            None
        if not file: return
        if file[-5:] == '.html' or file[-4:] == 'htm':
            text = self.TextEdit.document().toHtml()
        else: text = self.TextEdit.toPlainText()
        try:
            with codecs.open(file, 'w', encoding='utf8') as f:
                f.write(text)
                self.opened_file = file
                self.Window.setWindowTitle(self.ActualName+' ('+self.opened_file+')')
        except Exception as e:
            self.TextEdit.append('Impossibile salvare.')
            self.TextEdit.append('Eccezione:   '+str(e))
    def closefile(self):
        self.TextEdit.clear()
        self.opened_file = ''
        self.Window.setWindowTitle(self.ActualName)
    def defaultMenu(self, menu, app):
        #if not menu: menu = self.Menu
        #if not app: app = self.App
        file = menu.addMenu("&File")
        menu.addSeparator()
        apri = file.addAction('Apri...')
        apri.triggered.connect(self.openfile)
        apri.setShortcut(Qt.CTRL + Qt.Key_O)
        salva = file.addAction('Salva')
        salva.triggered.connect(self.save)
        salva.setShortcut(Qt.CTRL + Qt.Key_S)
        salvan = file.addAction('Salva con nome...')
        salvan.triggered.connect(self.savewithname)
        salvan.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_S)
        chiudi = file.addAction('Chiudi File')
        chiudi.triggered.connect(self.closefile)
        chiudi.setShortcut(Qt.CTRL + Qt.ALT + Qt.Key_Z)
        esci = file.addAction('Esci')
        esci.triggered.connect(app.quit)
        esci.setShortcut(Qt.CTRL + Qt.Key_Q)
    def setActualName(self, name):
        self.ActualName = name


############################### AVVIO PROGRAMMA ###############################

def main():
    CONTROLLER = Controller()
    CONTROLLER.main()

if __name__ == '__main__':
    main()
