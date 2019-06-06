# -*- coding: utf-8 -*-
"""
Python 3.5 Modality interface

Creato da Fabrizio Fubelli
"""

from PyQt5.QtWidgets import QMessageBox

class Mod:
    def __init__(self):
        self.directory = ''
        self.SMbutton = None
    def __rootCheck__(self):
        if not self.directory:
            alert = QMessageBox()
            alert.addButton(alert.Ok)
            alert.addButton(alert.Cancel)
            alert.setWindowTitle('Errore')
            alert.setText('Selezionare prima la directory Sorted_Music!')
            if alert.exec_() == alert.Ok:
                self.SMbutton.click()
                if not self.directory:
                    return False
            else: return False
        return True
    def __unableToOpenFile__(self, file):
        alert = QMessageBox()
        alert.addButton(alert.Ok)
        alert.setWindowTitle('Errore')
        alert.setText('Impossibile aprire il file '+file+'.')
        alert.exec_()
    def __createSubMenus__(self, menu, subMenu_List):
        ret = []
        for subMenu in subMenu_List:
            ret.append(menu.addMenu(subMenu))
        return ret
    def __createSubActions__(self, menu, subAction_List):
        ret = []
        for subAction in subAction_List:
            ret.append(menu.addAction(subAction))
        return ret
    def __createYesNoAlert__(self, title, infText, text, yesDef=False):
        alert = QMessageBox()
        alert.addButton(alert.Yes)
        alert.addButton(alert.No)
        if (yesDef): alert.setDefaultButton(alert.Yes)
        else: alert.setDefaultButton(alert.No)
        alert.setWindowTitle(title)
        if (infText): alert.setInformativeText(infText)
        if (text): alert.setText(text)
        if alert.exec_() == alert.Yes: return True
        return False