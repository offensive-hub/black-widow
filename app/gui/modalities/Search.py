# -*- coding: utf-8 -*-
"""
Python 3.5 Program to search the files

Creato da Fabrizio Fubelli
"""

import os, codecs

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from app.gui import MusicSort
from app.gui.modalities import Modality, Database

ALPHABET=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
SPECIAL='$'
__Articoli2__=['IL ', 'LO ', 'LA ', 'LE ', 'L  ', 'UN ']
__Articoli3__=['THE ','TH? ','GLI ','UNA ','UNO ','DEI ']
__A_acc__ = 'ÀÁÂÃÄÅÆĀĂĄǞǠǢǺǼȀȂȺΑΔΙӐӒӔᴀᴁᴧᴭḀẠẢẤẦẨẪẬẮẰẲẴẶἈἉἊἋἌἍἎἏᾸᾹᾺΆⱯ' #sorted
__E_acc__ = 'ÈÉÊËĒĔĖĘĚƎȄȆɆΈΕЀЁӖᴇᴱᴲḔḖḘḚḜẸẺẼẾỀỂỄỆἘἙἚἛἜἝῈΈΣ'            #sorted
__I_acc__ = 'ÌÍÎÏĨĪĬĮİƗǏȈȊ̀́̈͂ΊΙΪЇḬḮỈỊἸἹἺἻἼἽἾἿῘῙῚΊ'                    #sorted
__O_acc__ = 'ÒÓÔÕÖØŌŎŐŒƟƠǑǪǬǾȌȎȪȬȮȰΌΟОᴏᴓṌṎṐṒỌỎỐỒỔỖỘỚỜỞỠỢὈὉὊὋὌὍῸΌ'    #sorted
__U_acc__ = 'ÙÚÛÜŨŪŬŮŰŲǓǕǗǙǛȔȖɄЦᴜṲṴṶṸṺỤỦỨỪỬỮỰ'                       #sorted /*
__C_acc__ = 'С'
__H_acc__ = 'ΉΗ'
__M_acc__ = 'Μ'
__N_acc__ = 'ЙЛ'
__P_acc__ = 'Ρ'
__T_acc__ = 'ΤТ'                                                     #sorted */


def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size

def containsTag(searching_tag, exists_tag, convertStrings=False, isArtist=False, remTrat=True):
    s_tag = searching_tag
    e_tag = exists_tag
    if convertStrings:
        s_tag = __getComparableString__(s_tag, isArtist, remTrat)
        e_tag = __getComparableString__(e_tag, isArtist, remTrat)
    if s_tag in e_tag: return True
    lenS = len(s_tag)
    lenE = len(e_tag)
    if lenS > lenE: return False
    minEq = round(lenS/1.33333333333333337)
    q_S = 0
    for si in range(lenS):
        if si == '?': q_S += 1
    c_S = s_tag[0]
    for i in range(lenE):
        c_E = e_tag[i]
        if c_S == c_E or c_E == '?':
            pq = 0
            if c_E == '?' and c_S != '?': pq = 1
            try:
                eq, q = __containsTagCall__(s_tag[1:], e_tag[i+1:i+1+lenS])
                pq += q
                pq -= q_S
                if eq:
                    Eq = lenS - pq
                    if Eq >= minEq:
                        return True
            except:
                return False
    return False


def __containsTagCall__(searching_tag, exists_tag):
    if searching_tag in exists_tag: return (True, 0)
    q = 0
    for i in range(len(searching_tag)):
        c_S = searching_tag[i]
        c_E = exists_tag[i]
        if c_S != c_E:
            if c_E != '?': return (False, 0)
            q += 1
    return (True, q)

def __sosAnd__(s):
    s = s.upper()
    len_s = len(s)
    for i in range(len_s-2):
        if s[i:i+3] == ' & ':
            s = s[0:i]+' E '+s[i+3:]
        else:
            try:
                if s[i:i+5] == ' AND ':
                    s = s[0:i]+' E '+s[i+5:]
            except:
                continue
    return s

def __getComparableArtistName__(s):
    s = s.upper()
    try:
        if s[0:2] == 'I ': s = s[2:]
        elif s[0:3] in __Articoli2__: s = s[3:]
        elif s[0:4] in __Articoli3__: s = s[4:]
    except:
        None
    return s

def __getComparableString__(s, isArtist=False, remTrat=True):
    s_2 = s
    if isArtist: s_2 = __sosAnd__(s_2)
    new_s = ''
    for i in s_2:
        I = i.upper()
        if I in __A_acc__: new_s+='A'
        elif I in __E_acc__: new_s+='E'
        elif I in __I_acc__: new_s+='I'
        elif I in __O_acc__: new_s+='O'
        elif I in __U_acc__: new_s+='U'
        elif I in __C_acc__: new_s+='C'
        elif I in __H_acc__: new_s+='H'
        elif I in __N_acc__: new_s+='N'
        elif I in __M_acc__: new_s+='M'
        elif I in __P_acc__: new_s+='P'
        elif I in __T_acc__: new_s+='T'
        else:
            c = str(i.encode())[2:-1]
            if c[0] == '\\':
                new_s+='?'
                continue
            elif c == ' '[0] or c.isalpha():
                new_s+=c
            elif (remTrat and c == '-') or c == '_' or c == "'":
                new_s+=' '[0]
            else:
                try:
                    int(c)
                    new_s += c
                except:
                    if remTrat: new_s+='-'
                    else: new_s+='_'
    if isArtist: return __getComparableArtistName__(new_s)
    return new_s.upper()


class SearchMod(Modality.Mod):
    def __init__(self):
        self.NAME = 'Fabri MusicSearch'
        self.id = 2
        self.eDir = 'MUSIC_SORT/'
        self.name = "Modalità ricerca Musica"
        self.SearchFile = self.eDir+'DetailedFiles.np'
        self.OldSearchFile = self.eDir+'DetailedFiles.np'
        #self.ActualNames = ['gli Artisti di Album', 'gli Album', 'i titoli delle Canzoni', 'gli Artisti di Canzoni']
        self.directory = ''
        self.MB = 1048576
        self.Text_Artists = QTextEdit('')
        self.Text_Albums = QTextEdit('')
        self.Text_Songs = QTextEdit('')
        self.Text_AlbumArtists = QTextEdit('')
        self.Texts = [self.Text_AlbumArtists, self.Text_Albums, self.Text_Songs, self.Text_Artists]
        for t in self.Texts:
            t.setStyleSheet("background-color: red")
            t.setEnabled(False)
        self.DATABASE = Database.Database() # The Key is the File
        self.ATTRIBUTES = self.DATABASE.Attr[1:]
        self.DICTIONARY = None
    def __setAlbumArtistsFile__(self):
        self.__setFile__(0, 'gli Artisti di Album')
    def __setAlbumFile__(self):
        self.__setFile__(1, 'gli Album')
    def __setSongsFile__(self):
        self.__setFile__(2, 'i titoli delle Canzoni')
    def __setArtistsFile__(self):
        self.__setFile__(3, 'gli Artisti di Canzoni')
    def __setFile__(self, identifier, sname):
        file = ''
        try:
            file = QFileDialog.getOpenFileName(caption = 'Seleziona il file contenente la lista de'+sname+' da cercare')[0]
        except:
            None
        if not file: return
        self.SearchChecks[identifier].setChecked(True)
        self.checkSearchType(identifier)
        text = self.Texts[identifier]
        try:
            with codecs.open(file, 'r', encoding='utf8') as f:
                lines=f.readlines()
                i = 1
                for l in lines:
                    l = l.strip()
                    if l:
                        text.append(l)
                        i += 1
            self.Window.setWindowTitle(self.NAME+' ('+file+')')
        except Exception as e:
            text.append('Impossibile aprire il file selezionato.')
            text.append('Eccezione:   '+str(e))
    def __saveAlbumArtistsFile__(self):
        self.__saveFile__(0, 'Artista Album')
    def __saveAlbumFile__(self):
        self.__saveFile__(1, 'Album')
    def __saveSongsFile__(self):
        self.__saveFile__(2, 'Titolo Canzone')
    def __saveArtistsFile__(self):
        self.__saveFile__(3, 'Artista')
    def __saveFile__(self, identifier, sname):
        file = ''
        try:
            file = QFileDialog.getSaveFileName(caption = 'Salva lista canzoni trovate tramite ricerca per "'+sname+'"')[0]
        except:
            None
        if not file: return
        text = self.Texts[identifier].toPlainText()
        try:
            with codecs.open(file, 'w', encoding='utf8') as f:
                f.write(text)
        except Exception as e:
            alert = QMessageBox()
            alert.setWindowTitle('Errore')
            alert.setText('Impossibile salvare.')
            alert.setText('Eccezione:   '+str(e))
            alert.exec_()
    def __search__(self):
        if not self.__rootCheck__():
            return
        if not os.path.isfile(self.SearchFile):
            alert = QMessageBox()
            alert.addButton(alert.Yes)
            alert.addButton(alert.No)
            alert.setDefaultButton(alert.No);
            alert.setWindowTitle('Errore')
            t1 = 'Il file "DetailedFiles.np" non risulta essere nella directory "MUSIC_SORT".\n'
            t2 = """Se tale file non è stato spostato o rinominato dall'utente, questo dovrebbe creare e salvare la "Lista Dettagliata """
            t3 = 'tramite la modalità "Modifica tramite file."'
            alert.setInformativeText('Cercare manualmente il file "DetailedFiles.np" ?')
            alert.setText(t1+t2+t3)
            if alert.exec_() == alert.Yes:
                file = ''
                try:
                    file = QFileDialog.getOpenFileName(caption = 'Seleziona il file "DetailedFiles.np"')[0]
                except:
                    None
                if not file: return
                self.SearchFiles = file
            else:
                return
        # Ora self.SearchFile contiene l'url di "DetailedFiles.np"
        if not self.DICTIONARY or self.OldSearchFile != self.SearchFile:
            self.DATABASE = Database.Database() # The Key is the File
            self.DICTIONARY = self.DATABASE.getDictionary(self.SearchFile)
            self.OldSearchFile = self.SearchFile
        s = []
        for si in range(len(self.SearchChecks)):
            if self.SearchChecks[si].isChecked(): s.append(si)
        a_artists = []
        albums = []
        songs = []
        artists = []
        if 0 in s:
            AlbumArtistsToFind = self.Texts[0].toPlainText()
            a_artist = ''
            for i in AlbumArtistsToFind:
                if i == '\n':
                    a_artists.append(__getComparableString__(a_artist, True))
                    a_artist = ''
                else: a_artist += i
            a_artist = __getComparableString__(a_artist, True)
            if a_artist and a_artist not in a_artists: a_artists.append(a_artist)
            self.Texts[0].clear()
            print('\n\nNumero di Artisti di Album da cercare: '+str(len(a_artists)))
            print('Artisti di Album da cercare:')
            ai = 0
            for a in a_artists:
                print(str(ai)+')  '+a)
                ai += 1
            print('\nRicerca Artisti di Album in corso...')
        if 1 in s:
            AlbumsToFind = self.Texts[1].toPlainText()
            album = ''
            for i in AlbumsToFind:
                if i == '\n':
                    albums.append(__getComparableString__(album))
                    album = ''
                else: album += i
            album = __getComparableString__(album)
            if album and album not in albums: albums.append(album)
            self.Texts[1].clear()
            print('\n\nNumero di Album da cercare: '+str(len(albums)))
            print('Album da cercare:')
            ai = 0
            for a in albums:
                print(str(ai)+')  '+a)
                ai += 1
            print('\nRicerca Album in corso...')
        if 2 in s:
            SongsToFind = self.Texts[2].toPlainText()
            song = ''
            for i in SongsToFind:
                if i == '\n':
                    songs.append(__getComparableString__(song))
                    song = ''
                else: song += i
            song = __getComparableString__(song)
            if song not in songs: songs.append(song)
            self.Texts[2].clear()
            print('\n\nNumero di titoli di Canzoni da cercare: '+str(len(songs)))
            print('Titoli di Canzoni da cercare:')
            ai = 0
            for a in songs:
                print(str(ai)+')  '+a)
                ai += 1
            print('Ricerca Canzoni in corso...')
        if 3 in s:
            ArtistsToFind = self.Texts[3].toPlainText()
            artist = ''
            print('len(ArtistsToFind) = '+str(len(ArtistsToFind)))
            for i in ArtistsToFind:
                if i == '\n':
                    artists.append(__getComparableString__(artist, True))
                    artist = ''
                else: artist += i
            artist = __getComparableString__(artist, True)
            if artist and artist not in artists: artists.append(artist)

            self.Texts[3].clear()
            print('\n\nNumero di Artisti da cercare: '+str(len(artists)))
            print('Artisti da cercare:')
            ai = 1
            for a in artists:
                print(str(ai)+')  '+a)
                ai += 1
            print('Ricerca Artisti in corso...')

        # DICTIONARY items:  0=AlbumArtist   3=Album   5=Title   6=Artist
        if (len(a_artists) + len(albums) + len(songs) + len(artists)) > 0  :
            print('\nELEMENTI TROVATI:')
            AAlist, ALlist, Tlist, ARlist = [],[],[],[]
            for k in self.DICTIONARY.keys():
                items = self.DICTIONARY[k]
                AA, AL, T, AR = items[0], items[3], items[5], items[6]
                AA = __getComparableString__(AA, True)
                AL = __getComparableString__(AL)
                T = __getComparableString__(T)
                AR = __getComparableString__(AR, True)
                for al in albums:
                    if containsTag(al, AL): ALlist.append(k)
                #if AL in albums: ALlist.append(k)
                for t in songs:
                    if containsTag(t, T): Tlist.append(k)
                #if T in songs: Tlist.append(k)
                for aa in a_artists:
                    if containsTag(aa, AA):
                        print(AA)
                        AAlist.append(k)
                    #if aa in AA: AAlist.append(k)
                if AA != AR:
                    for ar in artists:
                        if containsTag(ar, AR): ARlist.append(k)
                        #if ar in AR: ARlist.append(k)
            AAlist.sort()
            ALlist.sort()
            Tlist.sort()
            ARlist.sort()
            for k1 in AAlist:
                self.Texts[0].append(k1)
            for k2 in ALlist:
                self.Texts[1].append(k2)
            for k3 in Tlist:
                self.Texts[2].append(k3)
            for k4 in ARlist:
                self.Texts[3].append(k4)
        print('\n\nDONE!')
    def setSearchButton(self, buttonSearch):
        self.buttonSearch = buttonSearch
        self.buttonSearch.clicked.connect(self.__search__)
        self.buttonSearch.setEnabled(False)
    # CALLED BY CONTROLLER
    def reset(self):
        self.Text.closefile()
        self.DICTIONARY = None
    def __searchMenu__(self):
        search = self.Menu.addMenu('Cerca')
        self.selectArtists = search.addAction('Artisti album')
        self.selectAlbums = search.addAction('Album')
        self.selectSongs = search.addAction('Canzoni')
        self.selectArtists = search.addAction('Artisti')
        self.searchMenus = [self.selectArtists, self.selectAlbums, self.selectSongs]
        for m in self.searchMenus: m.setCheckable(True)
    def setMenu(self):
        self.Menu.clear()
        #self.Text.defaultMenu(self.Menu, self.App)
        self.__searchMenu__()
        self.Menu.setStyleSheet("color: blue;"
                    "background-color: darkorange;"
                    "selection-color: orange;"
                    "selection-background-color: blue;"
                    )
        self.Menu.adjustSize()
    def checkSearchAlbumArtist(self):
        self.checkSearchType(0)
    def checkSearchAlbum(self):
        self.checkSearchType(1)
    def checkSearchSong(self):
        self.checkSearchType(2)
    def checkSearchArtist(self):
        self.checkSearchType(3)
    def checkSearchType(self, tipo):
        checkbox = self.SearchChecks[tipo]
        text = self.Texts[tipo]
        green = "color: lightgreen"
        if tipo == 3: green = "color: green"
        if checkbox.isChecked():
            checkbox.setStyleSheet(green)
            text.setStyleSheet("background-color: lightgreen")
            text.setEnabled(True)
            self.buttonSearch.setDisabled(False)
        else:
            checkbox.setStyleSheet("color: red")
            text.setStyleSheet("background-color: red")
            text.setEnabled(False)
            for c in self.SearchChecks:
                if c.isChecked(): return
            self.buttonSearch.setDisabled(True)
    def searchLayout(self, identifier, CheckBox, Button_Name):
        xLayout = QVBoxLayout()
        xLayoutUP = QHBoxLayout()
        xLayoutUP.setAlignment(Qt.AlignLeft)
        LoadFile = QPushButton('Carica lista '+Button_Name+' da file...')
        LoadFile.clicked.connect(self.LoadCallbacks[identifier])
        SaveFile = QPushButton('Salva lista '+Button_Name+'...')
        SaveFile.clicked.connect(self.SaveCallbacks[identifier])
        xLayoutUP.addWidget(CheckBox)
        xLayoutUP.addWidget(LoadFile)
        xLayoutUP.addWidget(SaveFile)
        xLayout.addLayout(xLayoutUP)
        xLayout.addWidget(self.Texts[identifier])
        return xLayout
    def setWindow(self, Height, SMbutton, textedit):
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
        dist = Height/50
        palette = QPalette()
        self.SMbutton = SMbutton
        tlayout.addWidget(SMbutton)
        B_search = QPushButton('CERCA')
        c_v2layout.addWidget(B_search)
        self.setSearchButton(B_search)
        palette.setBrush(QPalette.Background,QBrush(QPixmap("image/orange.jpg")))
        B_exit.clicked.connect(self.App.quit)
        c_h1layout.addLayout(c_h1layout_L)
        c_h1layout.addLayout(c_h1layout_R)
        clayout.addLayout(c_h1layout)
        clayout.addLayout(c_v2layout)
        clayout.addLayout(c_v3layout)
        tlayout.addWidget(B_exit)
        layout.addLayout(tlayout)
        layout.addLayout(clayout)
        signature = QLabel('Ricercatore Musicale di Fabrizio')
        signature.setAlignment(Qt.AlignRight)
        signature.setStyleSheet("color: red")
        layout.addWidget(signature)
        self.l_albumArtist = QCheckBox('Artisti album da cercare:')
        self.l_albumArtist.clicked.connect(self.checkSearchAlbumArtist)
        albumArtistLayout = self.searchLayout(0, self.l_albumArtist, 'Artisti di Album')
        layout.addLayout(albumArtistLayout)
        self.l_album = QCheckBox('Album da cercare:')
        self.l_album.clicked.connect(self.checkSearchAlbum)
        albumLayout =  self.searchLayout(1, self.l_album, 'Album')
        layout.addLayout(albumLayout)
        self.l_song = QCheckBox('Titoli canzoni da cercare:')
        self.l_song.clicked.connect(self.checkSearchSong)
        songLayout = self.searchLayout(2, self.l_song, 'titoli Canzoni')
        layout.addLayout(songLayout)
        self.l_artist = QCheckBox('Artisti da cercare:')
        self.l_artist.clicked.connect(self.checkSearchArtist)
        artistLayout = self.searchLayout(3, self.l_artist, 'Artisti')
        layout.addLayout(artistLayout)
        self.SearchChecks = [self.l_albumArtist, self.l_album, self.l_song, self.l_artist]
        for l in self.SearchChecks: l.setStyleSheet("color: red")
        self.TextEdit = textedit
        self.TextEdit.setMaximumSize(0, 0)
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
        self.LoadCallbacks=[self.__setAlbumArtistsFile__, self.__setAlbumFile__, self.__setSongsFile__, self.__setArtistsFile__]
        self.SaveCallbacks=[self.__saveAlbumArtistsFile__, self.__saveAlbumFile__, self.__saveSongsFile__, self.__saveArtistsFile__]
        self.App = app
        self.setWindow(height, SMbutton, textedit)
        self.setMenu()
