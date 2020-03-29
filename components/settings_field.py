from PyQt5 import QtWidgets, QtGui, QtCore

class SettingsField(QtWidgets.QLineEdit):
    
    def __init__(self, ui):
        super(SettingsField, self).__init__()
        
        self.ui = ui
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFrame(False)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setPlaceholderText("")
        
    def focusInEvent(self, event):
        self.ui.settingsFieldFocused(field = self)
        super(SettingsField, self).focusInEvent(event)

        
        
        