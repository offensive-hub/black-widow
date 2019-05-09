from PyQt5.QtWidgets import *

def open():
    main_gui = QApplication([])
    label = QLabel('Black Widow')
    label.show()
    main_gui.exec_()
