# -*- coding: utf-8 -*-
"""
Python 3.5 Program to search the files

Creato da Fabrizio Fubelli
"""

import os, codecs, sys

from datetime import datetime
from tinytag import TinyTag
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from app.gui import MusicSort
from app.gui.modalities import Modality

class EditByFileMod(Modality.Mod):
    def __init__(self):
        self.NAME = 'Fabri DatabaseFiles'
        self.id = 3
        self.name = 'Analisi e Creazione File per Database'
        self.Actual = ''
        self.directory = ''
        self.MB = 1048576
        self.eDir = 'MUSIC_SORT/'
        self.RECHECK_SONGS="MUSIC_SORT/RECHECK_SONGS"
        self.files_to_move = None
        self.MoveLog="MUSIC_SORT/SONGS_LOG_FILES/MoveLog.np"
    def selectFileByExcept(self, s):
        len_s = len(s)
        for i in range(len_s):
            if s[i:i+5] == 'FILE=':
                return s[i+5:-1]
        return s
    def selectFileByError(self, s):
        i = 0
        while i < len(s):
            l = s[i]
            i += 1
            try:
                int(l)
            except:
                if l == ')': return s[i+1:]
        return s
    def __setDetailedFiles__(self):
        file = None
        if self.__rootCheck__():
            ms = self.directory+'/MUSIC_SORT/DetailedFiles.np'
            if os.path.isfile(ms):
                file = ms
            else:
                alert = QMessageBox()
                alert.addButton(alert.Yes)
                alert.addButton(alert.No)
                alert.setDefaultButton(alert.No);
                alert.setWindowTitle('Errore')
                t1 = 'Il file "DetailedFiles.np" non risulta essere nella directory "MUSIC_SORT".\n'
                t2 = """Se tale file non è stato spostato o rinominato dall'utente, si dovrebbe creare e salvare la "Lista Dettagliata """
                alert.setInformativeText('Cercare manualmente il file "DetailedFiles.np" ?')
                alert.setText(t1+t2)
                if alert.exec_() == alert.Yes:
                    try:
                        file = QFileDialog.getOpenFileName(caption = 'Seleziona il file "DetailedFiles.np"')[0]
                    except:
                        None
                    if not file: return
                else: return
        else: return
        self.TextEdit.clear()
        if not file:
           self.TextEdit.append('Se il file "MUSIC_SORT/DetailedFiles.np" non è presente come dovrebbe, cliccare su "Crea lista dettagliata";')
           self.TextEdit.append('Terminata la creazione della lista dettagliata, si raccomanda di salvarla per completare la procedura;')
           self.TextEdit.append('\nInfine si potrà analizzare la lista per spostare in maniera ordinata eventuali file "corrotti".')
           return
        Lines=[]
        try:
            with codecs.open(file, 'r', encoding='utf8') as f:
                Lines=f.readlines()
        except Exception as e:
            self.TextEdit.append('Impossibile aprire il file selezionato.')
            self.TextEdit.append('Eccezione:   '+str(e))
        isErr = False
        isExcept = False
        self.files_to_move = []
        for line in Lines:
            line = line.strip()
            if line == 'ECCEZIONI:':
                isErr = False
                isExcept = True
                continue
            elif line == 'I SEGUENTI FILES RISULTANO INCOERENTI:':
                isErr = True
                isExcept = False
                continue
            if not line: continue
            filepath = ''
            if isExcept:
                filepath = self.selectFileByExcept(line)
            elif isErr:
                filepath = self.selectFileByError(line)
            else: continue
            self.files_to_move.append(filepath)
        self.Window.setWindowTitle(self.NAME+' ('+file+')')
        if len(self.files_to_move) > 0:
            self.Actual = 'Detailed'
            self.buttonStart.setText("SPOSTA I FILES DA RICONTROLLARE")
            self.buttonStart.setEnabled(True)
            self.TextEdit.append('FILES DA RICONTROLLARE:\n')
            for s in self.files_to_move:
                if s: self.TextEdit.append(s)
        else:
            self.TextEdit.append('NESSUN FILE DA RICONTROLLARE')
    def __start__(self):
        if self.Actual == 'Detailed':
            if not self.__rootCheck__(): return
            if not self.files_to_move:
                self.TextEdit.clear()
                self.TextEdit.append('Nessuna azione da fare!')
                return
            if len(self.files_to_move) == 0:
                self.TextEdit.clear()
                self.TextEdit.append('Nessun file da spostare.')
                return
            self.TextEdit.clear()
            self.__moveFiles__()
        elif self.Actual == 'List':
            if not self.__rootCheck__(): return
            if not os.path.isdir(self.eDir[-1]):
                try:
                    os.mkdir('MUSIC_SORT')
                except:
                    self.TextEdit.clear()
                    self.TextEdit.append('ECCEZIONE: Impossibile creare la directory "'+self.directory+'/MUSIC_SORT')
                    return
            with codecs.open(self.eDir+'DetailedFiles.np', 'w', encoding='utf8') as df:
                df.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                for l in self.MusicList:
                    df.write('\n'+l)
                if len(self.exceptions) > 0:
                    df.write('\n\nECCEZIONI:\n')
                    j = 1
                    for e in self.exceptions:
                        df.write(str(j)+') '+str(e)+'\n')
                        j+=1
                if len(self.errors) > 0:
                    df.write('\n\nI SEGUENTI FILES RISULTANO INCOERENTI:\n')
                    j = 1
                    for e in self.errors:
                        df.write(str(j)+') '+str(e)+'\n')
                        j+=1
            self.TextEdit.append('\nLista dettagliata salvata in:\n'+self.directory+'/MUSIC_SORT/DetailedFiles.np')
            self.Window.setWindowTitle(self.NAME+' ('+self.directory+'/MUSIC_SORT/DetailedFiles.np'+')')
        elif self.Actual == 'ListAfter':
            file = None
            try:
                file = QFileDialog.getSaveFileName()[0]
            except:
                None
            if not file: return
            with codecs.open(file, 'w', encoding='utf8') as df:
                df.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                for l in self.MusicList:
                    df.write('\n'+l)
                if len(self.exceptions) > 0:
                    df.write('\n\nECCEZIONI:\n')
                    j = 1
                    for e in self.exceptions:
                        df.write(str(j)+') '+str(e)+'\n')
                        j+=1
                if len(self.errors) > 0:
                    df.write('\n\nI SEGUENTI FILES RISULTANO INCOERENTI:\n')
                    j = 1
                    for e in self.errors:
                        df.write(str(j)+') '+str(e)+'\n')
                        j+=1
    def __moveFiles__(self):
        self.TextEdit.clear()
        #self.buttonStart.setEnabled(False)
        self.TextEdit.append('Spostamento dei files da ricontrollare in corso...\n')
        ren_to_write = ''
        for l in self.files_to_move:
            newfile = self.RECHECK_SONGS+'/'+l
            newdir = os.path.dirname(newfile)
            try:
                os.makedirs(newdir, exist_ok=True)
            except:
                self.TextEdit.append('\nECCEZIONE: Impossibile creare la directory "'+newdir+'"')
                continue
            try:
                os.rename(l, newfile)
            except:
                self.TextEdit.append('\nECCEZIONE: Impossibile spostare il file "'+l+'" in "'+newdir+'"')
                continue
            ren_to_write+='\n'+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+l+'  -->  '+newfile
        with codecs.open(self.MoveLog, 'a', encoding='utf8') as mv:
            mv.write(ren_to_write)
        self.TextEdit.append('\nI files da ricontrollare sono stati spostati in:\n'+self.directory+'/'+self.RECHECK_SONGS)
        self.TextEdit.append("\nLe modifiche apportate sono state segnate in:\n"+self.directory+"/"+self.MoveLog)
        self.TextEdit.append('\n\nDONE!')
    def __setMusicList__(self):
        file = None
        if self.__rootCheck__():
            ms = self.directory+'/MUSIC_SORT/SONGS_LOG_FILES/MusicList.np'
            if os.path.isfile(ms):
                file = ms
            else:
                t1 = 'Il file "MusicList.np" non risulta essere nella directory "MUSIC_SORT/SONGS_LOG_FILES".\n'
                t2 = """Se tale file non è stato spostato o rinominato dall'utente, si dovrebbe creare andando in modalità "Ordinamento Musica" e cliccando su START """
                if self.__createYesNoAlert__('Errore', 'Cercare manualmente il file "MusicList.np" ?', t1+t2):
                    try:
                        file = QFileDialog.getOpenFileName(caption = 'Seleziona il file "MusicList.np"')[0]
                    except:
                        None
                    if not file: return
        else: return
        if not file:
            self.TextEdit.clear()
            self.TextEdit.append('Se il file "/MUSIC_SORT/SONGS_LOG_FILES/MusicList.np" non è presente come dovrebbe:')
            self.TextEdit.append('andare in modalità "Ordinamento Musica" ed eseguire una scansione con START')
            return
        self.TextEdit.clear()
        self.exceptions = []
        self.errors = []
        self.MusicList = []
        ML = []
        try:
            with codecs.open(file, 'r', encoding='utf8') as f:
                ML=f.readlines()
        except Exception as e:
            self.TextEdit.append('Impossibile aprire il file selezionato.')
            self.TextEdit.append('Eccezione:   '+str(e))
        not_found = False
        files_errors = []
        total_files = []
        for i in range(1,len(ML)):
            l = ML[i]
            if not l: continue
            l = l.strip()
            if not os.path.isfile(l):
                self.exceptions.append('FILE NOT FOUND (FILE='+l+')')
                not_found = True
            if not_found: continue
            try:
                total_files.append((l, TinyTag.get(l)))
            except Exception as e:
                self.exceptions.append('TinyTag EXCEPTION: '+str(e)+' (FILE='+l+')')
        for ft in total_files:
            l = ft[0]
            tag = ft[1]
            albumartist = str(tag.albumartist)
            album = str(tag.album)
            artist = str(tag.artist)
            title = str(tag.title)
            disc_number = str(tag.disc)
            disc_total = str(tag.disc_total)
            track = str(tag.track)
            duration = str(tag.duration)
            bitrate = str(tag.bitrate)
            filesize = str(tag.filesize)
            last_modification = str(modification_date(l))
            a = album == '[non-album tracks]'
            b = albumartist != 'None' and albumartist != ' ' and albumartist != ''
            c = '[non-album tracks]' in l and '[non-album tracks]' not in album
            d = a and b
            if d or c:
                files_errors.append((l, album, albumartist))
                self.errors.append(l)
            line = 'FILE='+l+'   ALBUMARTIST='+albumartist+'   DISC_NUMBER='+disc_number+'   DISC_TOTAL='+disc_total+'   ALBUM='+album+'   TRACK='+track+'   TITLE='+title+'    ARTIST='+artist+'   DURATION='+duration+'   BITRATE='+bitrate+'   FILESIZE='+filesize+'   MODIFIED='+last_modification
            self.MusicList.append(line)
        self.Window.setWindowTitle(self.NAME+' ('+file+')')
        self.Actual = 'List'
        no_files = []
        if len(self.exceptions) > 0:
            toPrint = ''
            toPrint += '\nECCEZIONI:\n'
            j = 1
            for e in self.exceptions:
                ep = self.selectFileByExcept(e)
                if not os.path.isfile(ep):
                    no_files.append(ep)
                else:
                    toPrint += str(j)+') '+str(e)+'\n'
                    j+=1
            if len(no_files) == 0:
                self.TextEdit.append(toPrint)
        if len(self.errors) > 0:
            toPrint = ''
            toPrint += '\nI SEGUENTI FILES RISULTANO INCOERENTI:\n'
            j = 1
            for e in self.errors:
                toPrint += str(j)+') '+str(e)+'\n'
                j+=1
            self.TextEdit.append(toPrint)
            self.TextEdit.append('\nVERIFICA:\n')
            for e in files_errors:
                attr1="FILE="
                attr2="ALBUM="
                attr3="ALBUMARTIST="
                i = 1
                for attrs in e:
                    self.TextEdit.append(str(eval("attr"+str(i)))+'"'+str(attrs)+'"')
                    i+=1
                self.TextEdit.append(' ')
        if len(no_files) > 0:
            err_no_files1 = 'ATTENZIONE!!! La lista analizzata risulta non essere aggiornata con la raccolta musicale'
            err_no_files2 = 'andare nella modalità "Ordinamento Musica" ed eseguire una scansione cliccando su START.'
            err_no_files3 = '\nI files presenti in lista ma non sul disco, sono:'
            toPrint = err_no_files1+'\n'+err_no_files2+'\n'+err_no_files3
            self.TextEdit.clear()
            self.TextEdit.append(toPrint)
            for n in no_files:
                self.TextEdit.append(n)
        elif len(ML) > 0:
            self.buttonStart.setText('SALVA LISTA DETTAGLIATA')
            self.buttonStart.setEnabled(True)
        alert = QMessageBox()
        alert.addButton(alert.Yes)
        alert.addButton(alert.No)
        alert.setDefaultButton(alert.Yes);
        alert.setWindowTitle('Salva Lista Dettagliata')
        alert.setText('Salvare la lista dettagliata?\n(Consigliato: Sì)')
        if alert.exec_() == alert.Yes:
            self.buttonStart.click()
        if self.__createYesNoAlert__('Print', None, 'Visualizzare il file creato?'):
            for s in self.MusicList:
                if s: self.TextEdit.append(s)
        self.Actual = 'ListAfter'
        self.buttonDetailedFiles.setDisabled(False)
    def setDetailedFilesButton(self, buttonDetailedFiles):
        self.buttonDetailedFiles = buttonDetailedFiles
        self.buttonDetailedFiles.setDisabled(True)
        self.buttonDetailedFiles.clicked.connect(self.__setDetailedFiles__)
    def setStartButton(self, buttonStart):
        self.buttonStart = buttonStart
        self.buttonStart.setDisabled(True)
        self.buttonStart.clicked.connect(self.__start__)
    # CALLED BY CONTROLLER
    def reset(self):
        self.Actual = ''
        self.Text.closefile()
    def setMenu(self):
        self.Menu.clear()
        self.Text.defaultMenu(self.Menu, self.App)
        # funzione menu Search
        self.Menu.setStyleSheet("color: red;"
                    "background-color: lightgreen;"
                    "selection-color: lightgreen;"
                    "selection-background-color: red;"
                    )
        self.Menu.adjustSize()
    def setWindow(self, Height, SMbutton):
        self.Window.setWindowTitle(self.NAME)
        window = QWidget()
        layout = QVBoxLayout() # ALL (UP and DOWN)
        tlayout = QHBoxLayout() # ALL UP
        clayout = QHBoxLayout() # ALL DOWN
        B_exit = QPushButton('Esci')
        c_h1layout = QHBoxLayout() # DOWN_LEFT (ALL)
        c_v2layout = QVBoxLayout() # DOWN_CENTRAL (ALL)
        c_v3layout = QVBoxLayout() # DOWN_RIGHT (ALL)
        c_h1layout_L = QHBoxLayout() # DOWN_LEFT (sx)
        c_h1layout_R = QVBoxLayout() # DOWN_LEFT (dx)
        #signature = QLabel('')
        dist = Height/50

        self.SMbutton = SMbutton
        tlayout.addWidget(self.SMbutton)
        B_start = QPushButton('')
        c_v2layout.addWidget(B_start)
        self.setStartButton(B_start)

        B_MusicList = QPushButton('Crea lista dettagliata')   # Apri file "MusicList.np"
        c_h1layout_L.addWidget(B_MusicList)
        B_MusicList.clicked.connect(self.__setMusicList__)
        B_DetailedFiles = QPushButton('Analizza lista dettagliata')   # Apri file "DetailedFiles.np"'
        c_h1layout_L.addWidget(B_DetailedFiles)
        self.setDetailedFilesButton(B_DetailedFiles)

        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("image/green.jpg")))

        B_exit.clicked.connect(self.App.quit)
        c_h1layout.addLayout(c_h1layout_L)
        c_h1layout.addLayout(c_h1layout_R)
        clayout.addLayout(c_h1layout)
        clayout.addLayout(c_v2layout)
        clayout.addLayout(c_v3layout)
        tlayout.addWidget(B_exit)
        layout.addLayout(tlayout)
        layout.addLayout(clayout)
        layout.addWidget(self.TextEdit)
        layout.setContentsMargins(dist, dist, dist, dist)
        window.setLayout(layout)
        self.Window.setCentralWidget(window)
        self.Window.setPalette(palette)
    def setMod(self, win, textedit, height, menu, app, text, SMbutton):
        os.chdir(MusicSort.DIRECTORY)
        self.Text = text
        self.Text.setActualName(self.NAME)
        self.Window = win
        self.Menu = menu
        self.TextEdit = textedit
        self.App = app
        self.setMenu()
        self.setWindow(height, SMbutton)


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)
