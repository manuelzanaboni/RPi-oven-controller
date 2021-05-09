#!/usr/bin/python3
# coding: utf8

import sys
from ui.mainwindow import MainWindow
from PyQt5 import QtCore, QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    file = QtCore.QFile('./ui/stylesheet.qss')
    file.open(QtCore.QFile.ReadOnly)
    ss = bytes(file.readAll()).decode('latin-1')
    app.setStyleSheet(ss)

    w = MainWindow()
    w.showFullScreen()
#     w.show()
    sys.exit(app.exec_())