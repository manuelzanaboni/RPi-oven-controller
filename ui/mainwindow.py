#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from .oven_ui import Ui_MainWindow
from controller.oven_controller import OvenController
from controller.charts_controller import ChartsController
from components.switch import Switch
from components.settings_field import SettingsField
from math import floor, ceil

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
        
    notifySignal = pyqtSignal(str, bool, int)
    manageBurnerSignal = pyqtSignal(bool)
    manageValveSignal = pyqtSignal(bool)
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        """ Configuration dictionary """
        self.config = {}

        """ Timer initialization """
        self.timerSeconds = 0
        self.timer = QtCore.QTimer(parent = self)
        self.timerLCD.display("{0:02d}:{1:02d}".format(0, 0))

        self.fanMovie = QtGui.QMovie(":/resources/fan.gif", parent = self)
        
        """  Burner movie management """
        self.burnerLabel.setGeometry(QtCore.QRect(880, 230, 150, 175))
        self.fireMovie = QtGui.QMovie(":/resources/fire.gif", parent = self)
        self.fireMovie.setScaledSize(QtCore.QSize(150, 175))
        self.burnerLabel.setMovie(self.fireMovie)
        self.burnerLabel.hide()
        
        """  Burner valve movie management """
        self.burnerValveLabel.setGeometry(QtCore.QRect(830, 305, 75, 100))
        self.valveFireMovie = QtGui.QMovie(":/resources/fire.gif", parent = self)
        self.valveFireMovie.setScaledSize(QtCore.QSize(75, 100))
        self.burnerValveLabel.setMovie(self.valveFireMovie)
        self.burnerValveLabel.hide()
        
        """ Settings fields management """
        self.settingsFieldToEdit = None # holds reference of the focused field
        self.initialFieldsValues = {} # holds values of fields before the edit
        self.keypadFrame.hide()
        self.initializeSettingsFields()
        
        """ Populate config dictionary """
        try:
            self.config["checkPression"] = self.pressionSwitch.isChecked()
            self.config["inputPressionThreshold"] = int(self.inputPressionThreshold.text())
            self.config["persistData"] = self.persistDataSwitch.isChecked()
            self.config["inputValveThreshold"] = int(self.inputValveThreshold.text())
            self.config["inputInternalOpeningTime"] = int(self.inputInternalOpeningTime.text())
            self.config["inputUpperCheckerTime"] = int(self.inputUpperCheckerTime.text())
        except ValueError:
            raise RuntimeError('Could not cast config values.')
            
        """ Assign main controller """
        self.controller = OvenController(ui = self, config = self.config)
        
        """
        Charts Controller manages charts page.
        chartsLayout will be filled by that class.
        """
        self.chartsController = ChartsController(container = self.chartsLayout)
        
        self.connectActions()
        
    @pyqtSlot(str, bool, int)
    def notifySlot(self, message, critical, time):
        if critical:
            self.notifyCritical(message, time)
        else:
            self.notify(message, time)   
        
    @pyqtSlot(bool)
    def manageBurnerSlot(self, state):
        self.manageBurnerButtonAndLabel(state)
        
    @pyqtSlot(bool)
    def manageValveSlot(self, state):
        self.manageValveLabel(state)
        
    def initializeSettingsFields(self):
        self.pressionSwitch = Switch(thumb_radius=11, track_radius=15, parent = self)
        self.pressionSwitch.setChecked(True)
        self.settingsLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.pressionSwitch)
            
        self.inputPressionThreshold = SettingsField(ui = self)
        self.inputPressionThreshold.setText("30")
        self.inputPressionThreshold.setCursorPosition(2)
        self.inputPressionThreshold.setObjectName("inputPressionThreshold")
        self.settingsLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inputPressionThreshold)
        
        self.persistDataSwitch = Switch(thumb_radius=11, track_radius=15, parent = self)
        self.persistDataSwitch.setChecked(True)
        self.settingsLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.persistDataSwitch)
        
        self.inputValveThreshold = SettingsField(ui = self)
        self.inputValveThreshold.setText("30")
        self.inputValveThreshold.setCursorPosition(2)
        self.inputValveThreshold.setObjectName("inputValveThreshold")
        self.settingsLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.inputValveThreshold)
        
        self.inputInternalOpeningTime = SettingsField(ui = self)
        self.inputInternalOpeningTime.setText("5")
        self.inputInternalOpeningTime.setCursorPosition(1)
        self.inputInternalOpeningTime.setObjectName("inputInternalOpeningTime")
        self.settingsLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.inputInternalOpeningTime)
        
        self.inputUpperCheckerTime = SettingsField(ui = self)
        self.inputUpperCheckerTime.setText("120")
        self.inputUpperCheckerTime.setCursorPosition(3)
        self.inputUpperCheckerTime.setObjectName("inputUpperCheckerTime")
        self.settingsLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.inputUpperCheckerTime)
        
    def connectActions(self):
        """ Signal / Slot connections """
        self.notifySignal.connect(self.notifySlot)
        self.manageBurnerSignal.connect(self.manageBurnerSlot)
        self.manageValveSignal.connect(self.manageValveSlot)
        
        """ Manage buttons' action """
        self.burnerButton.clicked.connect(self.toggleBurner)

        self.burnerValveButton.clicked.connect(self.toggleBurnerValve)

        self.lightButton.clicked.connect(self.controller.toggleLight)

        self.steamButton.pressed.connect(self.controller.toggleSteam)
        self.steamButton.released.connect(self.controller.toggleSteam)

        self.fanMovie.frameChanged.connect(self.updateFanButton)
        self.fanMovie.start()
        self.fanMovie.stop()

        self.fanButton.clicked.connect(self.toggleFan)

        self.internalOpeningButton.clicked.connect(self.controller.toggleInternalOpening)

        self.externalOpeningButton.pressed.connect(self.controller.toggleExternalOpening)
        self.externalOpeningButton.released.connect(self.controller.toggleExternalOpening)
        
        self.rotisserieButton.clicked.connect(self.controller.toggleRotisserie)
        
        self.resistanceButton.clicked.connect(lambda state: self.toggleResistance(state))

        self.vacuumButton.clicked.connect(self.controller.toggleVacuum)

        self.horizontalSlider.valueChanged['int'].connect(self.thermostatLCD.display)
        self.horizontalSlider.sliderReleased.connect(self.setThermostatTemp)
        self.incrementThermostatButton.pressed.connect(self.incrementThermostat)
        self.decrementThermostatButton.pressed.connect(self.decrementThermostat)
        
        self.settings_resetPressionButton.clicked.connect(self.controller.calibratePressionSensors)
        self.alexaButton.clicked.connect(self.toggleAlexa)
        self.quitButton.clicked.connect(self.close)
        
        """ settings fields """
        self.pressionSwitch.toggled.connect(lambda state: self.pressionSwitchToggled(state))
        self.persistDataSwitch.toggled.connect(lambda state: self.persistDataSwitchToggled(state))
        """
        self.inputPressionThreshold, self.inputValveThreshold, self.inputInternalOpeningTime, self.inputUpperCheckerTime
        have been managed with custom QLineEdit, see SettingsField
        """
        
        """ Keypad connections """
        self.button0.clicked.connect(lambda: self.settingsFieldToEdit.insert("0"))
        self.button1.clicked.connect(lambda: self.settingsFieldToEdit.insert("1"))
        self.button2.clicked.connect(lambda: self.settingsFieldToEdit.insert("2"))
        self.button3.clicked.connect(lambda: self.settingsFieldToEdit.insert("3"))
        self.button4.clicked.connect(lambda: self.settingsFieldToEdit.insert("4"))
        self.button5.clicked.connect(lambda: self.settingsFieldToEdit.insert("5"))
        self.button6.clicked.connect(lambda: self.settingsFieldToEdit.insert("6"))
        self.button7.clicked.connect(lambda: self.settingsFieldToEdit.insert("7"))
        self.button8.clicked.connect(lambda: self.settingsFieldToEdit.insert("8"))
        self.button9.clicked.connect(lambda: self.settingsFieldToEdit.insert("9"))
        self.buttonDel.clicked.connect(lambda: self.settingsFieldToEdit.backspace())
        self.buttonOk.clicked.connect(self.confirmEdit)  

        """ timer connections """
        self.timer.timeout.connect(self.tick)
        self.decreaseTimerButton.clicked.connect(self.subtract10)
        self.increaseTimerButton.clicked.connect(self.add10)
        self.startTimerButton.clicked.connect(lambda: self.timer.start(1000) if self.timerSeconds > 0 else False)
        self.stopTimerButton.clicked.connect(self.timer.stop)
        self.resetTimerButton.clicked.connect(self.reset)
        
        """ charts connections """
        self.charts_ovenSerieButton.clicked.connect(lambda state: self.chartsController.toggleOvenSerie(state))
        self.charts_floorSerieButton.clicked.connect(lambda state: self.chartsController.toggleFloorSerie(state))
        self.charts_pufferSerieButton.clicked.connect(lambda state: self.chartsController.togglePufferSerie(state))
        self.charts_fumesSerieButton.clicked.connect(lambda state: self.chartsController.toggleFumesSerie(state))
        self.charts_realTimeButton.clicked.connect(lambda state: self.toggleRealTime(state))
        self.charts_lastHourButton.clicked.connect(lambda: self.chartsController.draw(interval = "hour"))
        self.charts_lastDayButton.clicked.connect(lambda: self.chartsController.draw(interval = "day"))
        self.charts_lastWeekButton.clicked.connect(lambda: self.chartsController.draw(interval = "week"))
        
        """ views linking """
        self.controller_settingsButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.controller_chartsButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.charts_settingsButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.charts_controllerButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.settings_controllerButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.settings_chartsButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        
    def toggleBurner(self):
        state = self.controller.toggleBurner()
        if state is not None:
            self.manageBurnerButtonAndLabel(state)
            
    def manageBurnerButtonAndLabel(self, state):
        if state:
            self.fireMovie.start()
            self.burnerLabel.show()
        else:
            self.fireMovie.stop()
            self.burnerLabel.hide()
    
    def toggleBurnerValve(self):
        self.controller.toggleBurnerValve()
        self.manageValveLabel(not self.valveFireMovie.state())
        
    def manageValveLabel(self, state):
        if state:
            self.valveFireMovie.start()
            self.burnerValveLabel.show()
        else:
            self.valveFireMovie.stop()
            self.burnerValveLabel.hide()        

    def updateFanButton(self):
        self.fanButton.setIcon(QtGui.QIcon(self.fanMovie.currentPixmap()))

    def toggleFan(self):
        ret = self.controller.toggleBurnerFan()
        if ret:
            if self.fanMovie.state():
                self.fanMovie.stop()
            else:
                self.fanMovie.start()
                
    def toggleResistance(self, state):
        if self.controller.thermostatCalling():
            self.controller.toggleResistance()
        else:
            self.resistanceButton.setChecked(not state)
        
    def toggleAlexa(self):  # TODO future feature
        pass

    def setThermostatTemp(self):
        value = self.thermostatLCD.value()
        self.controller.setThermostatValue(value)
        
    def incrementThermostat(self):
        value = self.horizontalSlider.value()
        
        if value < self.horizontalSlider.maximum():
            value = floor(value / 10) * 10 + 10 #math.floor
            self.horizontalSlider.setValue(value)
            self.setThermostatTemp()

    def decrementThermostat(self):
        value = self.horizontalSlider.value()
        
        if value > self.horizontalSlider.minimum():
            value = ceil(value / 10) * 10 - 10 # math.ceil
            self.horizontalSlider.setValue(value)
            self.setThermostatTemp()

    def pressionSwitchToggled(self, state):
        self.inputPressionThreshold.setEnabled(state)
        self.config["checkPression"] = state
        self.controller.setConfig(self.config)
        
    def persistDataSwitchToggled(self, state):
        self.config["persistData"] = state
        self.controller.setConfig(self.config)
    
    def settingsFieldFocused(self, field):
        self.settingsFieldToEdit = field
        
        if field is self.inputPressionThreshold and "inputPressionThreshold" not in self.initialFieldsValues:
            self.initialFieldsValues["inputPressionThreshold"] = (self.inputPressionThreshold, self.inputPressionThreshold.text())
        
        elif field is self.inputValveThreshold and "inputValveThreshold" not in self.initialFieldsValues:
            self.initialFieldsValues["inputValveThreshold"] = (self.inputValveThreshold, self.inputValveThreshold.text())
            
        elif field is self.inputInternalOpeningTime and "inputInternalOpeningTime" not in self.initialFieldsValues:
            self.initialFieldsValues["inputInternalOpeningTime"] = (self.inputInternalOpeningTime, self.inputInternalOpeningTime.text())
            
        elif field is self.inputUpperCheckerTime and "inputUpperCheckerTime" not in self.initialFieldsValues:
            self.initialFieldsValues["inputUpperCheckerTime"] = (self.inputUpperCheckerTime, self.inputUpperCheckerTime.text())
        
        if self.keypadFrame.isHidden():
            self.keypadFrame.show()
        
    def confirmEdit(self):
        if self.keypadFrame.isVisible():
            self.setFocus()
            self.keypadFrame.hide()
        
        for key in self.initialFieldsValues:
            text = self.initialFieldsValues[key][0].text()
            if self.initialFieldsValues[key][1] != text:
                if text == '':
                    self.initialFieldsValues[key][0].setText(self.initialFieldsValues[key][1])
                else:
                    self.updateConfig((key, self.initialFieldsValues[key][0].text()))
        
        self.controller.setConfig(self.config)
        
        self.settingsFieldToEdit = None
        self.initialFieldsValues = {}
        
    def updateConfig(self, data):
        try:
            value = int(data[1])
            self.config[data[0]] = value
        except ValueError:
            raise RuntimeError("Could not cast config values during update.")
        
    def toggleRealTime(self, state):
        self.charts_lastHourButton.setEnabled(not state)
        self.charts_lastDayButton.setEnabled(not state)
        self.charts_lastWeekButton.setEnabled(not state)

        if state:
            self.charts_realTimeButton.setText("Ferma tempo reale")
        else:
            self.charts_realTimeButton.setText("Tempo reale")
            
        self.controller.setRealTime(state)
        self.chartsController.toggleRealTimeTracking(state)
        
    def closeEvent(self, event):    # TODO check errors
        reply = QtWidgets.QMessageBox.question(self, 'Chiudi', "Sei sicuro di chiudere l'applicazione?", 
        QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.controller.close()
            event.accept()
        else:
            event.ignore()
            
    def notify(self, message, time):
        self.statusbar.setStyleSheet("font: 20px bold; color: #000000;")
        self.statusbar.showMessage(message, time)
        
    def notifyCritical(self, message, time):
        self.statusbar.setStyleSheet("font: 20px bold; color: #ED1B24;")
        self.statusbar.showMessage(message, time)

        """ Timer manager """
    def add10(self):
        self.timerSeconds += 10
        self.updateLCD()

    def subtract10(self):
        if self.timerSeconds >= 10:
            self.timerSeconds -= 10
        else:
            self.timerSeconds = 0
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
    """ End timer manager """