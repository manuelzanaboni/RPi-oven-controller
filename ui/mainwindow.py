#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from .oven_ui import Ui_MainWindow
from controller.oven_controller import OvenController
import math

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
        
    notifySignal = pyqtSignal(str, int)
    manageBurnerSignal = pyqtSignal(bool)
    
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
        
    @pyqtSlot(str, int)
    def notifySlot(self, message, time):
        self.notify(message, time)
        
    @pyqtSlot(bool)
    def manageBurnerSlot(self, state):
        self.manageBurnerButtonAndLabel(state)
        
    def connectActions(self):
        """
        Manage buttons' action
        """
        self.notifySignal.connect(self.notifySlot)
        self.manageBurnerSignal.connect(self.manageBurnerSlot)
        
        self.burnerButton.clicked.connect(self.toggleBurner)
        
        self.burnerValveButton.clicked.connect(self.toggleBurnerValve)

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

        self.horizontalSlider.valueChanged['int'].connect(self.thermostatLCD.display)
        self.horizontalSlider.sliderReleased.connect(self.setThermostatTemp)
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

    def toggleBurner(self):
        self.controller.toggleBurner()
        self.manageBurnerButtonAndLabel(not self.fireMovie.state())
            
    def manageBurnerButtonAndLabel(self, state):
        if state:
            self.fireMovie.start()
            self.burnerLabel.show()
        else:
            self.fireMovie.stop()
            self.burnerLabel.hide()
    
    def toggleBurnerValve(self):
        self.controller.toggleBurnerValve()

    def toggleLight(self):
        self.controller.toggleLight()

    def toggleSteam(self):
        self.controller.toggleSteam()

    def updateFanButton(self):
        self.fanButton.setIcon(QtGui.QIcon(self.fanMovie.currentPixmap()))

    def toggleFan(self):
        self.controller.toggleBurnerFan()
        if self.fanMovie.state():
            self.fanMovie.stop()
        else:
            self.fanMovie.start()

    def toggleInternalOpening(self):
        self.controller.toggleInternalOpening()

    def toggleExternalOpening(self):
        self.controller.toggleExternalOpening()

    def toggleAlexa(self):  # TODO future feature
        pass

    def setThermostatTemp(self):# TODO
        value = self.thermostatLCD.value()
        print(value)
        self.controller.setThermostatValue(value)
        
    def incrementThermostat(self):
        value = self.horizontalSlider.value()
        
        if value < self.horizontalSlider.maximum():
            value = math.floor(value / 10) * 10 + 10
            self.horizontalSlider.setValue(value)
            self.setThermostatTemp()

    def decrementThermostat(self):
        value = self.horizontalSlider.value()
        
        if value > self.horizontalSlider.minimum():
            value = math.ceil(value / 10) * 10 - 10
            self.horizontalSlider.setValue(value)
            self.setThermostatTemp()

    def closeEvent(self, event):    # TODO check errors
        reply = QtWidgets.QMessageBox.question(self, 'Chiudi', "Sei sicuro di chiudere l'applicazione?", 
        QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.controller.close()
            event.accept()
        else:
            event.ignore()
            
    def notify(self, message, time):
        self.statusbar.showMessage(message, time)

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
            self.controller.playAudio()

    def reset(self):
        self.timer.stop()
        self.timerSeconds = 0
        self.updateLCD()
#######################################