# -*- coding: utf-8 -*-
"""
Python 3.5 Program to sort the music files

Creato da Fabrizio Fubelli
"""

import os, codecs, shutil

from datetime import datetime
from tinytag import TinyTag
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from app.gui import MusicSort
from app.gui.modalities import Modality, Search

ALPHABET=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z', '0-9']
SPECIAL='$'

class SortingMod(Modality.Mod):
    def __init__(self):
        self.NAME = 'Fabri MusicSorting'
        self.id = 1
        self.name = 'Modalità ordinamento Musica'
        # fino a Sorted_Music
        self.directory=''
        self.AZ=None
        self.AZ_backup=''
        self.Menu = None
        # Cartella per canzoni non ordinate
        self.NO_SORTED_SONGS="MUSIC_SORT/NO_SORTED_SONGS"
        self.NO_AUDIO="MUSIC_SORT/NO_AUDIO"
        self.FLAC_FILES="MUSIC_SORT/FLAC"
        self.errSong = False
        self.renSong = False
        self.no_music = False
        self.exceptions=[]
        self.all_music_files=[]
        self.rename_files={}
        self.cp_FLAC = False
        self.mv_FLAC = False
        self.FLAC = []
        self.DIV_ALBUMS = {}
        self.div_a = False
        self.err = 'err'
        self.multi = 'multi'
        self.one = 'one'
        # Files di log
        self.MoveLog="MUSIC_SORT/SONGS_LOG_FILES/MoveLog.np"
        self.MusicList="MUSIC_SORT/SONGS_LOG_FILES/MusicList.np"
        self.RenameLog="MUSIC_SORT/SONGS_LOG_FILES/RenameLog.np"
    def inizialize(self, scrittura):
        # mi posiziono nella directory corretta
        os.chdir(self.directory)
        try:
            os.mkdir("MUSIC_SORT")
        except:
            None
        try:
            os.mkdir("MUSIC_SORT/SONGS_LOG_FILES")
        except:
            None
        if not scrittura:
            if self.AZ and self.AZ != self.AZ_backup:
                AZ_name = self.AZ[len(self.directory)+1:]
                self.MusicList="MUSIC_SORT/SONGS_LOG_FILES/MusicList_"+AZ_name+'.np'
                self.AZ_backup = self.AZ
            elif not self.AZ and self.AZ_backup:
                self.MusicList="MUSIC_SORT/SONGS_LOG_FILES/MusicList.np"
                self.AZ_backup = None
            return
        # creo le cartelle per i file da spostare o da creare
        try:
            os.mkdir(self.NO_SORTED_SONGS)
        except:
            None
        try:
            os.mkdir(self.NO_AUDIO)
        except:
            None
        # creo i file di log
        with open(self.MoveLog, 'a') as mv:
            mv.write('')
        with open(self.RenameLog, 'a') as ren:
            ren.write('')
    def name_check(self, s1, s2):
        # s1 può contenere caratteri speciali
        # s2 e' il nome della cartella dell'artista
        if (s1 == None and s2 == None): return True
        if (len(s1) != len(s2)): return False
        for i in range(len(s1)):
            if (s2[i] != "_" and s2[i] != s1[i]): return False
        return True
    def non_album_check(self, song, artist, artist_path):
        # song = nome canzone (senza path)
        # artist = nome artista (senza path)
        # artist_path = path (ex: "A/Artista")
        try:
            tag = TinyTag.get(artist_path+"/"+song)
        except Exception as e:
            self.exceptions.append('TinyTag Exception: impossibile ottenere il tag della canzone:\n'+artist_path+"/"+song)
            return True
        if tag.album == "[non-album tracks]" and tag.albumartist == None and self.name_check(tag.artist, artist):
            return True
        return False
    def not_in_position(self, errSongs, artist, artist_path):
        # errSongs = lista nomi canzoni (senza path)
        # artist = nome artista (senza path)
        # artist_path = path (ex: "A/Artista")
        self.errSong = True
        mov_to_write = ''
        for es in errSongs:
            if (es[-4:] != ".mp3" and es[-5:] != ".flac"):
                oldpath = self.spec_filename(artist_path+"/"+es)
                newdir = self.spec_filename(self.NO_AUDIO+'/'+artist)
                newpath = newdir+'/'+self.spec_filename(es)
                if not os.path.isdir(newdir):
                    try:
                        os.mkdir(newdir)
                    except Exception as e:
                        print('errore durante la creazione di directory')
                        self.exceptions.append("couldn't create directory:  "+newdir)
                        continue
                os.replace(oldpath, newpath)
                mov_to_write += ("\n"+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+oldpath+"  -->  "+newpath)
            elif self.non_album_check(es, artist, artist_path):
                newdir = self.spec_filename(artist_path+"/[non-album tracks]")
                try:
                    if not os.path.isdir(newdir): os.mkdir(newdir)
                except:
                    print('errore durante la creazione di directory')
                    self.exceptions.append("couldn't create directory:  "+newdir)
                    continue
                oldpath = self.spec_filename(artist_path+"/"+es)
                newpath = self.spec_filename(artist_path+"/[non-album tracks]/"+es)
                if (os.path.isfile(newpath)):
                    best_song = self.best_file_audio(newpath, oldpath)
                    if best_song == newpath:
                        try:
                            os.replace(oldpath, newpath)
                            mov_to_write+='\n'+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+newpath+'  -->  DELETED'
                            mov_to_write+='\n'+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+oldpath+'  -->  '+newpath
                        except Exception as e:
                            self.exceptions.append(e)
                            continue
                    else:
                        try:
                            os.remove(oldpath)
                            mov_to_write+='\n'+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+oldpath+'  -->  DELETED'
                        except Exception as e:
                            self.exceptions.append(e)
                            continue
                else :
                    os.rename(oldpath, newpath)
                    mov_to_write+="\n"+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+oldpath+"  -->  "+newpath
            else:
                newpath = self.spec_filename(self.NO_SORTED_SONGS+"/"+artist)
                try:
                    if not os.path.isdir(newpath): os.mkdir(newpath)
                except:
                    print('errore durante la creazione di directory')
                    self.exceptions.append("couldn't create directory:  "+newpath)
                    continue
                oldpath = self.spec_filename(artist_path+"/"+es)
                newpath = newpath+'/'+self.spec_filename(es)
                os.rename(oldpath, newpath)
                mov_to_write += "\n"+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+oldpath+"  -->  "+newpath
        with codecs.open(self.MoveLog, 'a', encoding='utf8') as mv:
            try:
                mv.write(mov_to_write)
            except Exception as e:
                print('errore durante la scrittura in file di log')
                self.exceptions.append(e.args)
    def no_music_file(self, filepath, artist, album, filename):
        l1 = self.NO_AUDIO+'/'+self.spec_filename(artist)
        l2 = l1+'/'+self.spec_filename(album)
        try:
            if not os.path.isdir(l1):
                os.mkdir(l1)
            if not os.path.isdir(l2):
                os.mkdir(l2)
        except:
            print('errore durante la creazione di directory')
            self.exceptions.append("couldn't create directory:  "+l2)
            return
        oldfile = self.spec_filename(filepath)
        newfile = l2+'/'+self.spec_filename(filename)
        try:
            os.replace(oldfile, newfile)
        except:
            print('errore durante lo spostamento di un file')
            self.exceptions.append("couldn't move file:  "+self.spec_filename(oldfile))
            return
        mov_to_write = "\n"+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+oldfile+"  -->  "+newfile
        with codecs.open(self.MoveLog, 'a', encoding='utf8') as mv:
            try:
                mv.write(mov_to_write)
            except Exception as e:
                print('errore durante la scrittura in file di log')
                self.exceptions.append(e.args)
    def spec_filename(self, file):
        new_filename = file.encode('utf8')
        return str(new_filename.decode("utf-8", "ignore"))
    def folder_in_album(self, artista, nome_album, album_dir):
        # sposta l'album in NO_SORTED_SONGS
        # artista = nome artista (senza path)
        # nome_album = nome dell'album da spostare
        # album_dir = path dell' album da spostare
        newpath = self.spec_filename(self.NO_SORTED_SONGS+"/"+artista)
        #newdir = spec_filename(directory+"/"+newpath)
        try:
            if not os.path.isdir(newpath): os.mkdir(newpath)
        except Exception as e:
            print('errore durante la creazione di directory')
            self.exceptions.append("couldn't create directory:  "+newpath)
        olddir = self.spec_filename(album_dir)
        newdir = self.spec_filename(newpath+"/"+nome_album)
        os.rename(olddir, newdir)
        with codecs.open(self.MoveLog, 'a', encoding='utf8') as mv:
            try:
                mv.write("\n"+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+olddir+"  -->  "+newdir)
            except Exception as e:
                print('errore durante la scrittura in file di log')
                self.exceptions.append(e.args)
    def best_file_audio(self, file1, file2):
        '''Ritorna una lista contenente i due files in input. Il primo della lista
        è quello con la qualità migliore'''
        tag1 = None
        tag2 = None
        try:
            tag1 = TinyTag.get(file1)
        except:
            tag1 = None
        try:
            tag2 = TinyTag.get(file2)
        except:
            tag2 = None
        if tag1 == None and tag2 == None:
            self.exceptions.append('TinyTag Exception: impossibile ottenere il tag della canzone:\n'+str(file1))
            self.exceptions.append('TinyTag Exception: impossibile ottenere il tag della canzone:\n'+str(file2))
            return file1
        elif tag1 == None:
            return tag2
        elif tag2 == None:
            return tag1
        if tag1.bitrate == tag2.bitrate:
            if tag1.filesize >= tag2.filesize: return file1
            else: return file2
        elif tag1.bitrate >= tag2.bitrate: return file1
        else: return file2
    def number_of_files(self, path=None, songs=False, iniziale=False):
        ''' Ritorna il numero di cartelle dentro la directory path'''
        n_sub_files = 0
        subdirs = None
        if path != None: subdirs = os.listdir(path)
        else:
            subdirs = os.listdir()
            path=''
        for f in subdirs:
            if os.path.isdir(path+'/'+f):
                if iniziale and len(f) <= 3:
                    n_sub_files += 1
                elif not iniziale: n_sub_files += 1
            elif songs:
                if f[-4:] == '.mp3' or  f[-5:] == '.flac':
                    n_sub_files += 1
        return n_sub_files
    def wichType(self, song):
        a = song[0]
        try:
            int(a)
        except:
            return self.err
        b = song[1]
        c = song[2]
        d = song[3]
        e = song[4]
        f = song[5]
        try:
            int(b)
        except:
            if b == '-':
                try:
                    int(c)
                    int(d)
                    if e == ' ': return self.multi
                    else:
                        int(e)
                        if f == ' ': return self.multi
                except:
                    return self.err
            return self.err
        if c == ' ': return self.one
        if c == '-':
            try:
                int(d)
                int(e)
                if f == ' ': return self.multi
                else:
                    int(f)
                    g = song[6]
                    if g == ' ': return self.multi
            except:
                return self.err
            return self.multi
        try:
            int(c)
            if d == ' ': return self.one
        except:
            return self.err
        return self.err

    def start(self):
        print('\nstart (in lettura\\scrittura)')
        tree=''
        #tree+=('\n'+
        IND_LIST=os.listdir()
        self.new_double_album = set()
        for i in IND_LIST:  # i = Iniziale artista
            if (self.AZ and self.directory+"/"+i != self.AZ): continue
            if os.path.isdir(i) and len(i) <= 3:
                LEN_ARTISTS=self.number_of_files(path=i, songs=False, iniziale=False)
                IND_ARTIST=0
                tree+=('\n'+"INIZIALE: "+i)
                if LEN_ARTISTS > 0: tree+=('\n'+"     |")
                for a in os.listdir(i): # a = ARTISTA
                    artista=i+"/"+a
                    if not (os.path.isdir(artista)): continue
                    IND_ARTIST+=1
                    ind_ind='|'
                    if IND_ARTIST >= LEN_ARTISTS: ind_ind = ' '
                    tree+=('\n'+"     |---- ARTISTA:  "+artista)
                    ALBUMS=os.listdir(artista)
                    LEN_ALBUMS=len(ALBUMS)
                    IND_ALBUMS=0
                    a_ind="|"
                    if (LEN_ALBUMS == 0): a_ind = " "
                    tree+=('\n'+"     "+ind_ind+"           "+a_ind)
                    errSongs=[] # contiene solo i nomi delle canzoni X in artista/X
                    for ac in ALBUMS:   # ac = ALBUM ( o canzone )
                        IND_ALBUMS+=1
                        album_canzone = artista+"/"+ac
                        ind="|"
                        if (IND_ALBUMS == LEN_ALBUMS): ind = " "
                        songs_in_album=[]
                        if os.path.isdir(album_canzone):
                            tree+=('\n'+"     "+ind_ind+"           |---- ALBUM:    "+album_canzone)
                            songs_in_album=os.listdir(album_canzone)
                            if self.number_of_files(album_canzone, True, False) > 0:
                                tree+=('\n'+"     "+ind_ind+"           "+ind+"          |")
                        else:
                            tree+=('\n'+"     "+ind_ind+"           |---- NO-DIR:   "+album_canzone)
                            errSongs.append(ac)
                            continue
                        tipo = None
                        a_finded = False
                        for c in songs_in_album:    # c = CANZONE
                            canzone = album_canzone+"/"+c
                            if os.path.isdir(canzone):
                                self.folder_in_album(a, ac, album_canzone)
                                tree+=('\n'+"     "+ind_ind+"           "+ind+"          |---- FOLDER: "+canzone)
                            elif c[-4:] == ".mp3":
                                tree+=('\n'+"     "+ind_ind+"           "+ind+"          |---- MP3:    "+canzone)
                                ccp = c[-7:-4]
                                try:
                                    int(ccp[1])
                                except:
                                    if a_finded or ac == '[non-album tracks]': continue
                                    if tipo == None:
                                        tipo = self.wichType(c)
                                        if tipo == self.err:
                                            a_finded = True
                                            self.div_a = True
                                            self.DIV_ALBUMS[album_canzone] = [a, ac]
                                    else:
                                        tipo2 = self.wichType(c)
                                        if tipo2 == self.err or tipo2 != tipo:
                                            a_finded = True
                                            self.div_a = True
                                            self.DIV_ALBUMS[album_canzone] = [a, ac]
                                    continue
                                if (ccp[0] == "(" and ccp[2] == ")"):
                                    dx = -7
                                    if (c[-8] == " "):
                                        dx = -8
                                    oldname = self.spec_filename(canzone)
                                    newname = self.spec_filename(canzone[:dx]+canzone[-4:])
                                    self.rename_files[oldname] = newname
                                else:                                   # new
                                    if a_finded or ac == '[non-album tracks]': continue
                                    if tipo == None:
                                        tipo = self.wichType(c)
                                        if tipo == self.err:
                                            a_finded = True
                                            self.div_a = True
                                            self.DIV_ALBUMS[album_canzone] = [a, ac]
                                    else:
                                        tipo2 = self.wichType(c)
                                        if tipo2 == self.err or tipo2 != tipo:
                                            a_finded = True
                                            self.div_a = True
                                            self.DIV_ALBUMS[album_canzone] = [a, ac]
                            elif c[-5:] == ".flac":
                                tree+=('\n'+"     "+ind_ind+"           "+ind+"          |---- FLAC:   "+canzone)
                                ccp = c[-8:-5]
                                try:
                                    int(ccp[1])
                                except:
                                    if (self.cp_FLAC or self.mv_FLAC): self.FLAC.append([canzone, a, ac, c])
                                    if a_finded or ac == '[non-album tracks]': continue
                                    if tipo == None:
                                        tipo = self.wichType(c)
                                        if tipo == self.err:
                                            a_finded = True
                                            self.div_a = True
                                            self.DIV_ALBUMS[album_canzone] = [a, ac]
                                    else:
                                        tipo2 = self.wichType(c)
                                        if tipo2 == self.err or tipo2 != tipo:
                                            a_finded = True
                                            self.div_a = True
                                            self.DIV_ALBUMS[album_canzone] = [a, ac]
                                    continue
                                if (ccp[0] == "(" and ccp[2] == ")"):
                                    dx = -8
                                    if (c[-8] == " "):
                                        dx = -9
                                    oldname = self.spec_filename(canzone)
                                    newname = self.spec_filename(canzone[:dx]+canzone[-5:])
                                    self.rename_files[oldname] = newname
                                    if (self.cp_FLAC or self.mv_FLAC): self.FLAC.append([canzone, a, ac, c])
                                else:
                                    if (self.cp_FLAC or self.mv_FLAC): self.FLAC.append([canzone, a, ac, c])
                                    if a_finded or ac == '[non-album tracks]': continue
                                    if tipo == None:
                                        tipo = self.wichType(c)
                                        if tipo == self.err:
                                            a_finded = True
                                            self.div_a = True
                                            self.DIV_ALBUMS[album_canzone] = [a, ac]
                                    else:
                                        tipo2 = self.wichType(c)
                                        if tipo2 == self.err or tipo2 != tipo:
                                            a_finded = True
                                            self.div_a = True
                                            self.DIV_ALBUMS[album_canzone] = [a, ac]
                            else:
                                t = c[-4:]  # t = type
                                if t == '.jpg' or t == '.gif' or t == '.png':
                                    continue
                                self.no_music = True
                                self.no_music_file(canzone, a, ac, c)
                        tree+=('\n'+"     "+ind_ind+"           "+ind)
                    if len(errSongs) > 0:
                        self.not_in_position(errSongs, a, artista)
            else:continue
            tree+=('\n'+'')
        self.finalize(True, tree)
    def visit_only_start(self):
        print('\nstart (in sola lettura)')
        tree=''
        IND_LIST=os.listdir()
        self.new_double_album = set()
        for i in IND_LIST:
            if (self.AZ and self.directory+"/"+i != self.AZ): continue
            if os.path.isdir(i) and len(i) <= 3:
                LEN_ARTISTS=self.number_of_files(path=i, songs=False, iniziale=False)
                IND_ARTIST=0
                tree+=('\n'+"INIZIALE: "+i)
                if LEN_ARTISTS > 0: tree+=('\n'+"     |")
                for a in os.listdir(i):
                    artista=i+"/"+a
                    if not (os.path.isdir(artista)): continue
                    IND_ARTIST+=1
                    ind_ind='|'
                    if IND_ARTIST >= LEN_ARTISTS: ind_ind = ' '
                    tree+=('\n'+"     |---- ARTISTA:  "+artista)
                    ALBUMS=os.listdir(artista)
                    LEN_ALBUMS=len(ALBUMS)
                    IND_ALBUMS=0
                    a_ind="|"
                    if (LEN_ALBUMS == 0): a_ind = " "
                    tree+=('\n'+"     "+ind_ind+"           "+a_ind)
                    for ac in ALBUMS:
                        IND_ALBUMS+=1
                        album_canzone=artista+"/"+ac
                        ind="|"
                        if (IND_ALBUMS == LEN_ALBUMS): ind = " "
                        songs_in_album=[]
                        if os.path.isdir(album_canzone):
                            tree+=('\n'+"     "+ind_ind+"           |---- ALBUM:    "+album_canzone)
                            songs_in_album=os.listdir(album_canzone)
                            if self.number_of_files(album_canzone, True, False) > 0:
                                tree+=('\n'+"     "+ind_ind+"           "+ind+"          |")
                        else:
                            tree+=('\n'+"     "+ind_ind+"           |---- NO-DIR:   "+album_canzone)
                            if ac[-4:] == ".mp3" or ac[-5:] == ".flac":
                                self.all_music_files.append(album_canzone)
                            self.errSong = True
                        tipo = None
                        artist_in_name = None
                        for c in songs_in_album:
                            canzone = album_canzone+"/"+c

                            # Controlla se vi sono più versioni dello stesso album in un'unica cartella
                            #try:
                                #if ' - ' not in TinyTag.get(canzone).title:
                            if artist_in_name == None:
                                artist_in_name = ' - ' in c
                            elif artist_in_name:
                                if ' - ' not in c: self.new_double_album.add(album_canzone) # "album_canzone" va ricontrollato
                            else:
                                if ' - ' in c: self.new_double_album.add(album_canzone)
                            #except: None
                            if os.path.isdir(canzone):
                                tree+=('\n'+"     "+ind_ind+"           "+ind+"          |---- FOLDER: "+canzone)
                                continue
                            if c[-4:] == ".mp3" or c[-5:] == ".flac":
                                if artist_in_name == None:
                                    artist_in_name = ' - ' in c
                                elif artist_in_name:
                                    if ' - ' not in c: self.new_double_album.add(album_canzone) # "album_canzone" va ricontrollato
                                else:
                                    if ' - ' in c: self.new_double_album.add(album_canzone)
                                if c[-4:] == ".mp3":
                                    tree+=('\n'+"     "+ind_ind+"           "+ind+"          |---- MP3:    "+canzone)
                                    self.all_music_files.append(canzone)
                                    ccp = c[-7:-4]
                                    try:
                                        int(ccp[1])
                                    except:
                                        if not self.div_a and ac != '[non-album tracks]':
                                            if tipo == None:
                                                tipo = self.wichType(c)
                                                if tipo == self.err: self.div_a = True
                                            else:
                                                tipo2 = self.wichType(c)
                                                if tipo2 != tipo or tipo2 == self.err:
                                                    self.div_a = True                  # new
                                        continue
                                    if (ccp[0] == "(" and ccp[2] == ")"):
                                        self.rename_files[c] = ccp
                                    else:
                                        if not self.div_a and ac != '[non-album tracks]':
                                            if tipo == None:
                                                tipo = self.wichType(c)
                                                if tipo == self.err: self.div_a = True
                                            else:
                                                tipo2 = self.wichType(c)
                                                if tipo2 != tipo or tipo2 == self.err:
                                                    self.div_a = True                  # new
                                elif c[-5:] == ".flac":
                                    tree+=('\n'+"     "+ind_ind+"           "+ind+"          |---- FLAC:   "+canzone)
                                    self.all_music_files.append(canzone)
                                    if (self.cp_FLAC or self.mv_FLAC): self.FLAC.append([canzone, a, ac, c])
                                    ccp = c[-8:-5]
                                    try:
                                        int(ccp[1])
                                    except:
                                        if not self.div_a and ac != '[non-album tracks]':
                                            if tipo == None:
                                                tipo = self.wichType(c)
                                                if tipo == self.err: self.div_a = True
                                            else:
                                                tipo2 = self.wichType(c)
                                                if tipo2 != tipo or tipo2 == self.err:
                                                    self.div_a = True                  # new
                                        continue
                                    if (ccp[0] == "(" and ccp[2] == ")" and len(self.rename_files) == 0):
                                        self.rename_files[c] = ccp
                                    else:
                                        if not self.div_a and ac != '[non-album tracks]':
                                            if tipo == None:
                                                tipo = self.wichType(c)
                                                if tipo == self.err: self.div_a = True
                                            else:
                                                tipo2 = self.wichType(c)
                                                if tipo2 != tipo or tipo2 == self.err:
                                                    self.div_a = True                  # new
                            else:
                                t = c[-4:]  # t = type
                                if t == '.jpg' or t == '.gif' or t == '.png':
                                    continue
                                self.no_music = True
                        tree+=('\n'+"     "+ind_ind+"           "+ind)
            else: continue
            tree+=('\n'+'')
        self.finalize(False, tree)
    def finalize(self, scrittura, tree):
        if self.__createYesNoAlert__("Print", None, "Desideri visualizzare l'albero dei tuoi file musicali?"):
            self.TextEdit.append(tree)
            self.TextEdit.append('\n')
        if len(self.new_double_album) > 0:
            real_err = set()
            self.new_double_album = list(self.new_double_album)
            self.new_double_album.sort()

            for album_dir in self.new_double_album:
                s_list = os.listdir(album_dir)
                artist_in_name = None
                for s_name in s_list:
                    if (s_name[-4:] != ".mp3" and s_name[-5:] != ".flac"): continue
                    if ' - ' not in TinyTag.get(album_dir+"/"+s_name).title:
                        if artist_in_name == None:
                            artist_in_name = ' - ' in s_name
                        elif artist_in_name:
                            if ' - ' not in s_name: real_err.add(album_dir) # "album_canzone" va ricontrollato
                        else:
                            if ' - ' in s_name: real_err.add(album_dir)

            if len(real_err) > 0:
                self.TextEdit.append("TROVATE PIU' VERSIONI DI ALCUNI ALBUM NELLA STESSA CARTELLA:")
                real_err = list(real_err)
                real_err.sort()
                for re in real_err:
                    self.TextEdit.append(re)
                self.TextEdit.append('\n')

        if self.errSong or self.no_music or self.div_a:
            m = "TROVATI FILES NON POSIZIONATI CORRETTAMENTE"
            print(m)
            self.TextEdit.append(m)
            if scrittura:
                msg="\nAvvio riposizionamento files..."
                if len(self.DIV_ALBUMS) > 0:
                    for albumpath in self.DIV_ALBUMS:
                        ar_al = self.DIV_ALBUMS[albumpath]
                        ar = self.spec_filename(ar_al[0])
                        al = self.spec_filename(ar_al[1])
                        newpath1 = self.NO_SORTED_SONGS+'/'+ar
                        if not os.path.isdir(newpath1):
                            try:
                                os.mkdir(newpath1)
                            except Exception as e:
                                print('errore durante la creazione di directory')
                                self.exceptions.append("couldn't create directory:  "+newpath1)
                                continue
                        oldpath = self.spec_filename(albumpath)
                        newpath = newpath1+'/'+al
                        os.rename(oldpath, newpath)
                        with codecs.open(self.MoveLog, 'a', encoding='utf8') as mv:
                            try:
                                mv.write("\n"+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+oldpath+"  -->  "+newpath)
                            except Exception as e:
                                print('errore durante la scrittura in file di log')
                                self.exceptions.append(e.args)
                msg2="\n\nLe canzoni da riordinare sono state spostate in:\n"+self.directory+"/"+self.NO_SORTED_SONGS
                msg3='\nI files diversi da ".mp3", ".flac", .jpg", ".png" e ".gif" sono stati spostati in:\n'+self.directory+"/"+self.NO_AUDIO
                msg4="\nLe modifiche apportate sono state segnate in:\n"+self.directory+"/"+self.MoveLog
                self.TextEdit.append(msg)
                self.TextEdit.append(msg2)
                self.TextEdit.append(msg3)
                self.TextEdit.append(msg4)
            self.TextEdit.append('\n\n')
        if len(self.rename_files) > 0:
            print('TROVATE CANZONI CON NOMI DI TIPO "nome_canzone (1).mp3"')
            self.TextEdit.append('TROVATE CANZONI CON NOMI DI TIPO "nome_canzone (1).mp3"')
            if scrittura:
                msg="\nAvvio rinominazione canzoni..."
                msg2="\n\nLe modifiche apportate sono state segnate in:\n"+self.directory+"/"+self.RenameLog
                self.TextEdit.append(msg)
                self.TextEdit.append(msg2)
                rename_exceptions = self.finelize_rename_files()
                if len(rename_exceptions) > 0:
                    self.TextEdit.append("\n\nSi sono verificate le seguenti eccezioni:")
                    ie = 0
                    for e in rename_exceptions:
                        ie += 1
                        self.TextEdit.append(str(ie)+")   "+str(e))
            self.TextEdit.append('\n\n')
        if (self.mv_FLAC or self.cp_FLAC) and len(self.FLAC) > 0:
            if not os.path.isdir(self.FLAC_FILES):
                try:
                    os.mkdir(self.FLAC_FILES)
                except:
                    print('errore durante la creazione di directory')
                    self.exceptions.append("couldn't create directory:  "+self.FLAC_FILES)
            f_action = 'COPIARE'
            f_action_2 = 'la copia'
            f_action_3 = 'copia'
            f_action_en = 'copy'
            if self.mv_FLAC:
                f_action = 'SPOSTARE'
                f_action_2 = 'lo spostamento'
                f_action_3 = 'spostamento'
                f_action_en = 'move'
            print('TROVATI FLAC DA '+f_action)
            self.TextEdit.append('\n\n\nTROVATI FLAC DA '+f_action)
            self.TextEdit.append("\nAvvio "+f_action_3+" flac...")
            for flac_details in self.FLAC:   # flac_details = [pathfile, artista, album, canzone]
                artist = self.spec_filename(flac_details[1])
                album = self.spec_filename(flac_details[2])
                canzone = self.spec_filename(flac_details[3])
                oldpath = self.spec_filename(flac_details[0])
                l1 = self.FLAC_FILES+'/'+artist
                l2 = l1+'/'+album
                try:
                    if not os.path.isdir(l1):
                        os.mkdir(l1)
                    if not os.path.isdir(l2):
                        os.mkdir(l2)
                except:
                    print('errore durante la creazione di directory')
                    self.exceptions.append("couldn't create directory:  "+l2)
                    continue
                newpath = l2+'/'+canzone
                try:
                    if self.cp_FLAC:
                        shutil.copy2(oldpath, l2)
                    elif self.mv_FLAC:
                        os.replace(oldpath, newpath)
                except:
                    print('errore durante '+f_action_2+' di un file')
                    self.exceptions.append("couldn't "+f_action_en+" file:  "+oldpath)
                    continue
                if self.mv_FLAC:
                    mov_to_write = "\n"+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+oldpath+"  -->  "+newpath
                    with codecs.open(self.MoveLog, 'a', encoding='utf8') as mv:
                        try:
                            mv.write(mov_to_write)
                        except Exception as e:
                            print('errore durante la scrittura in file di log')
                            self.exceptions.append(e.args)
            if self.mv_FLAC: self.TextEdit.append("\n\nLe modifiche apportate sono state segnate in:\n"+self.directory+"/"+self.MoveLog)
        if len(self.exceptions) > 0:
            self.TextEdit.append("\n\nSi sono verificate le seguenti eccezioni:")
            ie = 0
            for e in self.exceptions:
                ie += 1
                self.TextEdit.append(str(ie)+")   "+str(e))
        if (len(self.all_music_files) > 0 and not scrittura and not self.mv_FLAC):
            self.TextEdit.append("\n\n\nDato che non sono state apportate modifiche ai files, verrà salvata la lista delle canzoni in:")
            self.TextEdit.append("\n"+self.directory+"/"+self.MusicList)
            print("\n\nAvvio scrittura lista canzoni...")
            self.TextEdit.append("\n\nAvvio scrittura lista canzoni...")
            with codecs.open(self.MusicList, 'w', encoding='utf8') as ml:
                ml.write(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
                iex = 0
                for mf in self.all_music_files:
                    try:
                        ml.write('\n'+mf)
                    except Exception as e:
                        iex += 1
                        self.TextEdit.append("\n\n\nECCEZIONE ["+str(iex)+"]:    "+str(e))
                        self.TextEdit.append("\nL' eccezione si è generata mentre il programma stava cercando di scrivere questa stringa all'interno della lista delle canzoni:\n")
                        self.TextEdit.append(mf)
                        continue
        print("\n\n\nDONE!")
        self.TextEdit.append("\n\n\nDONE!")
    def finelize_rename_files(self):
        ren_exceptions = []
        ren_to_write = ''
        for oldname in self.rename_files:
            newname = self.rename_files[oldname]
            if (os.path.isfile(newname)):
                # se già esiste il file senza '(x)'
                # newname = file senza '(x)' esistente
                # oldname = file con '(x)'
                best_song = self.best_file_audio(newname, oldname)
                if best_song == oldname:
                    try:
                        os.replace(oldname, newname)
                        ren_to_write+='\n'+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+newname+'  -->  DELETED'
                        ren_to_write+='\n'+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+oldname+'  -->  '+newname
                    except Exception as e:
                        ren_exceptions.append(e)
                        continue
                else:
                    try:
                        os.remove(oldname)
                        ren_to_write+='\n'+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+oldname+'  -->  DELETED'
                    except Exception as e:
                        ren_exceptions.append(e)
                        continue
            else:
                try:
                    os.rename(oldname, newname)
                    ren_to_write+='\n'+datetime.now().strftime("%d-%m-%Y %H:%M:%S")+' '+oldname+'  -->  '+newname
                except Exception as e:
                    ren_exceptions.append(e)
                    continue
        with codecs.open(self.RenameLog, 'a', encoding='utf8') as rl:
            rl.write(ren_to_write)
        return ren_exceptions
    def reset(self):
        self.errSong=False
        self.renSong=False
        self.no_music = False
        self.exceptions=[]
        self.all_music_files=[]
        self.rename_files={}
        self.cp_FLAC=False
        self.mv_FLAC=False
        self.FLAC = []
        self.Text.closefile()
        self.DIV_ALBUMS = {}
        self.div_a = False
        self.new_double_album = set()
    # GRAPHIC
    def select_dir_callback(self):
        try:
            newdir = str(QFileDialog.getExistingDirectory())
        except:
            None
        if newdir:
            self.directory=newdir
            self.TextEdit.clear()
            self.TextEdit.append("Directory principale selezionata:\n"+self.directory)
            if self.AZ:
                self.TextEdit.append("\nDirectory secondaria:\n"+self.AZ)
    def select_AZ_callback(self):
        try:
            newdir = str(QFileDialog.getExistingDirectory())
        except:
            None
        if newdir:
            #print("newdir = "+newdir+"\ndirectory = "+directory)
            if newdir == self.directory: return
            self.AZ=newdir
            self.TextEdit.clear()
            if self.directory:
                self.TextEdit.append("Directory primaria:\n"+self.directory)
            self.TextEdit.append("\nDirectory secondaria selezionata:\n"+self.AZ)
    def start_callback(self):
        self.TextEdit.clear()
        if not self.__rootCheck__():
            return
        self.reset()
        if self.copy_FLAC.checkState(): self.cp_FLAC = True
        elif self.move_FLAC.checkState(): self.mv_FLAC = True
        msg="Avvio programma in sola lettura..."
        if self.mv_FLAC or self.CB_edit.checkState(): msg="Avvio programma in lettura/scrittura..."
        if (self.CB_edit.checkState()):
            print(msg)
            self.TextEdit.append(msg)
            self.inizialize(True)
            print("\nROOT = "+self.directory+"\n")
            self.TextEdit.append("\nROOT = "+self.directory+"\n")
            self.start()
        else:
            print(msg)
            self.TextEdit.append(msg)
            self.inizialize(False)
            print("\nROOT = "+self.directory+"\n")
            self.TextEdit.append("\nROOT = "+self.directory+"\n")
            self.visit_only_start()
    def clearAZ_callback(self):
        self.AZ = ''
        self.TextEdit.clear()
        if self.directory:
            self.TextEdit.append("Directory primaria:\n"+self.directory)
    def copyUncheck(self):
        self.copy_FLAC.setChecked(False)
        self.menu_cFLAC.setChecked(False)
        self.menu_mFLAC.setChecked(self.move_FLAC.isChecked())
    def moveUncheck(self):
        self.move_FLAC.setChecked(False)
        self.menu_mFLAC.setChecked(False)
        self.menu_cFLAC.setChecked(self.copy_FLAC.isChecked())
    def menu_Cunchecked(self):
        self.copy_FLAC.setChecked(False)
        self.menu_cFLAC.setChecked(False)
        self.move_FLAC.setChecked(self.menu_mFLAC.isChecked())
    def menu_Munchecked(self):
        self.move_FLAC.setChecked(False)
        self.menu_mFLAC.setChecked(False)
        self.copy_FLAC.setChecked(self.menu_cFLAC.isChecked())
    def recoursiveMove(self, src, dst):
        if os.path.isdir(dst):
            for subfile in os.listdir(src):
                sub = src+'/'+subfile
                self.recoursiveMove(sub, dst+'/'+subfile)
        elif os.path.isfile(src):
            if os.path.isfile(dst):
                if src[-4:] != '.mp3' and src[-5] != '.flac':
                    os.replace(src, dst)
                else:
                    try:
                        t = self.best_file_audio(src, dst)
                        if t == src:
                            os.replace(src, dst)
                        else: os.remove(src)
                    except Exception as e:
                        self.TextEdit.append('\nECCEZIONE: '+str(e))
            else:
                os.rename(src, dst)
        else:
            os.rename(src, dst)
    def isEmptyFolder(self, directory):
        if os.path.isfile(directory): return False
        elif not os.path.isdir(directory): return False
        for f in os.listdir(directory):
            if not self.isEmptyFolder(directory+'/'+f): return False
        return True
    def sortRoot(self):
        self.TextEdit.clear()
        if not self.__rootCheck__():
            return
        self.TextEdit.clear()
        self.TextEdit.append('Ordinamento Root in corso...\n')
        for artist in os.listdir():
            if 'MUSIC_' not in artist and artist not in ALPHABET and artist != SPECIAL:
                i = artist[0]
                try:
                    int(i)
                    i = '0-9'
                except:
                    i = i.upper()
                newdir = ''
                if i in ALPHABET: newdir = i
                else: newdir = SPECIAL
                if not os.path.isdir(i):
                    try:
                        os.mkdir(i)
                    except Exception as e:
                        self.TextEdit.append('\nECCEZIONE: Impossibile spostare la directory "'+i+'"')
                        self.TextEdit.append(+str(e))
                        continue
                newpath = newdir+'/'+artist
                try:
                    self.recoursiveMove(artist, newpath)
                    self.TextEdit.append('Spostato "'+artist+'" in "'+newdir+'"')
                except Exception as e:
                    self.TextEdit.append('\nECCEZIONE: Impossibile spostare la directory "'+artist+'"')
                    self.TextEdit.append(+str(e))
                    continue
                if self.isEmptyFolder(artist):
                    shutil.rmtree(artist)
    # CALLED BY CONTROLLER
    def setMenu(self):
        self.Menu.clear()
        self.Text.defaultMenu(self.Menu, self.App)
        paths = self.Menu.addMenu('&Directory')
        self.Menu.addSeparator()
        pri = paths.addAction('Imposta cartella Primaria')
        pri.triggered.connect(self.SMbutton.click)
        paths.addSeparator()
        sec = paths.addMenu('Cartella Secondaria')
        sec_new = sec.addAction('Imposta cartella Secondaria')
        sec_rem = sec.addAction('Dimentica cartella Secondaria')
        sec_new.triggered.connect(self.select_AZ_callback)
        sec_rem.triggered.connect(self.clearAZ_callback)
        opzioni = self.Menu.addMenu('&Opzioni')
        self.Menu.addSeparator()
        flac = opzioni.addMenu('Flac')
        self.menu_cFLAC = flac.addAction("Copiare i FLAC in un'altra cartella")
        self.menu_mFLAC = flac.addAction("Spostare i FLAC in un'altra cartella")
        self.menu_cFLAC.setCheckable(True)
        self.menu_mFLAC.setCheckable(True)
        self.menu_cFLAC.triggered.connect(self.menu_Munchecked)
        self.menu_mFLAC.triggered.connect(self.menu_Cunchecked)

        files = opzioni.addMenu('Root')
        moveFolderInInitial = files.addAction('Ordinare la root')
        moveFolderInInitial.triggered.connect(self.sortRoot)
        self.Menu.setStyleSheet("color: yellow;"
                            "background-color: darkblue;"
                            "selection-color: blue;"
                            "selection-background-color: yellow;"
                            )
        self.Menu.adjustSize()
    def setWindow(self, Height, SMbutton):
        self.Window.setWindowTitle(self.NAME)
        window = QWidget()
        layout = QVBoxLayout() # ALL (UP and DOWN)
        tlayout = QHBoxLayout() # ALL UP
        clayout = QHBoxLayout() # ALL DOWN
        B_exit = QPushButton('Esci')
        c_h1layout = QHBoxLayout() # LEFT (ALL)
        c_v2layout = QVBoxLayout() # CENTRAL (ALL)
        c_v3layout = QVBoxLayout() # RIGHT (ALL)
        c_h1layout_L = QHBoxLayout() # LEFT (sx)
        c_h1layout_R = QVBoxLayout() # LEFT (dx)
        signature = QLabel()
        dist = Height/50
        palette = QPalette()

        self.SMbutton = SMbutton
        B_select_AZ = QPushButton('Iniziale ($, 0-9, A...Z)')
        B_start = QPushButton('START')
        self.CB_edit = QCheckBox('Modificare i files')
        self.copy_FLAC = QCheckBox("Copiare i FLAC in un'altra cartella")
        self.move_FLAC = QCheckBox("Spostare i FLAC in un'altra cartella")
        B_clear_AZ = QPushButton("Dimentica directory 'Iniziale ($, 0-9, A...Z)'")
        self.CB_edit.setStyleSheet("color: red")
        self.copy_FLAC.setStyleSheet("color: orange")
        self.move_FLAC.setStyleSheet("color: darkorange")
        self.copy_FLAC.clicked.connect(self.moveUncheck)
        self.move_FLAC.clicked.connect(self.copyUncheck)
        B_select_AZ.clicked.connect(self.select_AZ_callback)
        B_start.clicked.connect(self.start_callback)
        B_clear_AZ.clicked.connect(self.clearAZ_callback)
        tlayout.addWidget(self.SMbutton)
        tlayout.addWidget(B_select_AZ)
        tlayout.addWidget(B_clear_AZ)
        c_h1layout_L.addWidget(self.CB_edit)
        c_h1layout_L.setAlignment(Qt.AlignCenter)
        c_h1layout_R.addWidget(self.copy_FLAC)
        c_h1layout_R.addWidget(self.move_FLAC)
        c_h1layout_R.setAlignment(Qt.AlignCenter)
        c_v2layout.addWidget(B_start)
        signature.setText('Ordinatore Musicale di Fabrizio')
        signature.setTextFormat(Qt.TextFormat(3))
        signature.setStyleSheet("color: white")
        c_v3layout.addWidget(signature)
        c_v3layout.setAlignment(Qt.AlignCenter)
        palette.setBrush(QPalette.Background,QBrush(QPixmap("image/blu.jpg")))

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
        self.TextEdit = textedit
        self.Menu = menu
        self.App = app
        self.setWindow(height, SMbutton)
        self.setMenu()
