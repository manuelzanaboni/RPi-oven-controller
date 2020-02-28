#!/usr/bin/python3
# coding: utf8

from PyQt5 import QtCore, QtGui, QtWidgets
from .oven_ui import Ui_MainWindow
from controller.oven_controller import OvenController
import math

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.controller = OvenController(self)  # set controller

        self.timerSeconds = 0
        self.timer = QtCore.QTimer()
        self.timerLCD.display("{0:02d}:{1:02d}".format(0, 0))

        self.fanMovie = QtGui.QMovie(":/src/fan.gif")
        
        self.burnerLabel = QtWidgets.QLabel(self.centralwidget)
        self.burnerLabel.move(520, 280)
        self.burnerLabel.setText("")
        self.burnerLabel.setObjectName("burnerLabel")

        self.fireMovie = QtGui.QMovie(":/src/fire.gif")
        self.fireMovie.setScaledSize(QtCore.QSize(160, 160))
        self.burnerLabel.setMovie(self.fireMovie)
        self.burnerLabel.hide()

        self.connectActions()

    def connectActions(self):
        """
        Manage buttons' action
        """
        self.horizontalSlider.valueChanged['int'].connect(self.thermostatLCD.display)

        self.burnerButton.clicked.connect(self.toggleBurner)

        self.lightButton.clicked.connect(self.toggleLight)

        self.steamButton.pressed.connect(self.toggleSteam)
        self.steamButton.released.connect(self.toggleSteam)

        self.fanMovie.frameChanged.connect(self.updateFanButton)
        self.fanMovie.start()
        self.fanMovie.stop()

        self.fanButton.clicked.connect(self.toggleFan)

        self.internalOpeningButton.clicked.connect(self.toggleInternalOpening)

        self.externalOpeningButton.pressed.connect(self.toggleExternalOpening)
        self.externalOpeningButton.released.connect(self.toggleExternalOpening)

        self.incrementThermostatButton.pressed.connect(self.incrementThermostat)
        self.decrementThermostatButton.pressed.connect(self.decrementThermostat)

        self.alexaButton.clicked.connect(self.toggleAlexa)

        self.quitButton.clicked.connect(self.close)

        self.timer.timeout.connect(self.tick)
        self.decreaseTimerButton.clicked.connect(self.subtract10)
        self.increaseTimerButton.clicked.connect(self.add10)
        self.startTimerButton.clicked.connect(lambda: self.timer.start(1000) if self.timerSeconds > 0 else False)
        self.stopTimerButton.clicked.connect(self.timer.stop)
        self.resetTimerButton.clicked.connect(self.reset)

    def toggleBurner(self):  # TODO
        if self.fireMovie.state():
            self.fireMovie.stop()
            self.burnerLabel.hide()
        else:
            self.fireMovie.start()
            self.burnerLabel.show()

    def toggleLight(self):  # TODO
        self.controller.toggleLight()

    def toggleSteam(self):  # TODO
        self.controller.toggleSteam()

    def updateFanButton(self):
        self.fanButton.setIcon(QtGui.QIcon(self.fanMovie.currentPixmap()))

    def toggleFan(self):  # TODO
        self.controller.toggleBurnerFan()
        if self.fanMovie.state():
            self.fanMovie.stop()
        else:
            self.fanMovie.start()

    def toggleInternalOpening(self):    # TODO
        self.controller.toggleInternalOpening()

    def toggleExternalOpening(self):    # TODO
        self.controller.toggleExternalOpening()

    def toggleAlexa(self):  # TODO future feature
        pass

    def incrementThermostat(self):    # TODO
        value = self.horizontalSlider.value()
        value = math.floor(value / 10) * 10 + 10
        self.horizontalSlider.setValue(value)

    def decrementThermostat(self):    # TODO
        value = self.horizontalSlider.value()
        value = math.ceil(value / 10) * 10 - 10
        self.horizontalSlider.setValue(value)

    def closeEvent(self, event):    # TODO check errors
        reply = QtWidgets.QMessageBox.question(self, 'Chiudi', "Sei sicuro di chiudere l'applicazione?", 
        QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.controller.close()
            event.accept()
        else:
            event.ignore()
            
    def notify(self, message):
        self.statusbar.showMessage(message, 4000)

############# TIMER MANAGER #############
    def add10(self):
        self.timerSeconds += 10
        self.updateLCD()        
    
    def subtract10(self):
        if self.timerSeconds >= 10:
            self.timerSeconds -= 10
            self.updateLCD()

    def updateLCD(self):
        min = self.timerSeconds // 60
        if min > 0:
            sec = self.timerSeconds % 60
        else:
            sec = self.timerSeconds

        time = ("{0:02d}:{1:02d}".format(min, sec))
        self.timerLCD.display(time)
    
    def tick(self):
        if self.timerSeconds >= 1:
            self.timerSeconds -= 1
            self.updateLCD()
        else:
            self.timer.stop()

    def reset(self):
        self.timer.stop()
        self.timerSeconds = 0
        self.updateLCD()
#######################################