from PyQt5.QtWidgets import *

from app.gui import MusicSort

def open():
    MusicSort.main()
    return
    main_gui = QApplication([])
    label = QLabel('Black Widow')
    label.show()
    main_gui.exec_()
