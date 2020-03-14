#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import subprocess

import utils.default_gpio as PIN
from utils.messages import OVEN_CONTROLLER_MSGS as MSG
from .burner_controller import BurnerController
from .sens_reader import SensReader
from .rpi_fan import FanController
from .internal_opening_controller import InternalOpeningController

AUDIO_PATH = 'resources/audio.mp3' # where to find audio file to be played
UPPER_SAFETY_PRESSION_THRESHOLD = 500 # (Pa) delta pression threshold. if greater, burner must turn off.

class OvenController(object):
    def __init__(self, ui):
        self.ui = ui

        self.__ovenTemp = 0 # holds oven internal temperature
        self.__floorTemp = 0 # holds oven's floor temperature
        self.__pufferTemp = 0 # holds puffer temperature (water)
        self.__fumesTemp = 0 # holds exhaust fumes temperture
        self.__deltaPression = 0 # holds pression variation
        
        self.__setPoint = self.ui.horizontalSlider.minimum() # system set point

        # state variables
        self.__burner = False
        self.__burnerValve = False
        self.__light = False
        self.__steam = False
        self.__burnerFan = False
        self.__externalOpening = False

        # initialize Relay GPIO
        GPIO.setmode(GPIO.BCM)
        gpioList = [PIN.RELAY1_BURNER, PIN.RELAY2_BURNER_VALVE, PIN.RELAY3_BURNER_FAN,
                    PIN.RELAY4_LIGHT, PIN.RELAY5_STEAM, PIN.RELAY6_INT_OPENING,
                    PIN.RELAY7_EST_OPENING, PIN.RELAY8_RPI_FAN]
        for i in gpioList:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

        # threads
        self.__threads = []

        self.__burnerController = BurnerController(controller = self)
        self.__threads.append(self.__burnerController)
        self.__burnerController.start()
            
        self.__sensReader = SensReader(controller = self)
        self.__threads.append(self.__sensReader)
        self.__sensReader.start()

        self.__fanController = FanController(controller = self)
        self.__threads.append(self.__fanController)
        self.__fanController.start()

    def getOvenTemp(self):
        return self.__ovenTemp
    
    def getDeltaPression(self):
        return self.__deltaPression
    
    def getSetPoint(self):
        return self.__setPoint
    
    def getBurnerValve(self):
        return self.__burnerValve
    
    def getLowerThermostatBound(self):
        return self.ui.horizontalSlider.minimum()

    def setData(self, ovenTemp, floorTemp, pufferTemp, fumesTemp, deltaPression):
        if ovenTemp is not None:
            self.__ovenTemp = ovenTemp
            self.ui.ovenLCD.display(self.__ovenTemp)

        if floorTemp is not None:
            self.__floorTemp = floorTemp
            self.ui.floorLCD.display(self.__floorTemp)

        if pufferTemp is not None:
            self.__pufferTemp = pufferTemp
            self.ui.pufferLCD.display(self.__pufferTemp)

        if fumesTemp is not None:
            self.__fumesTemp = fumesTemp
            self.ui.fumesLCD.display(self.__fumesTemp)

        if deltaPression is not None:
            self.__deltaPression = deltaPression
            self.ui.pressionLCD.display(self.__deltaPression)
            
            if self.__deltaPression >= UPPER_SAFETY_PRESSION_THRESHOLD: # react to possible blockage
                self.notifyCritical(MSG["burner_blockage"])
                self.manageBurnerButtonAndLabel(False)
                self.__burnerController.pause()

    def toggleBurner(self):
        self.__burner = not self.__burner
        
        if self.__burner:
            self.__burnerController.resume()
        else:
            self.__burnerController.pause()
            
    def toggleBurnerValve(self, thermostatOverride = None):
        if thermostatOverride is not None:
            self.__burnerValve = thermostatOverride
            self.ui.burnerValveButton.setChecked(thermostatOverride)
        else:
            self.__burnerValve = not self.__burnerValve
        
        if self.__burnerValve:
            self.ui.burnerValveLabel.show()
            GPIO.output(PIN.RELAY2_BURNER_VALVE, GPIO.LOW)
            self.notify(MSG["valve_on"])
        else:
            self.ui.burnerValveLabel.hide()
            GPIO.output(PIN.RELAY2_BURNER_VALVE, GPIO.HIGH)
            self.notify(MSG["valve_off"])
        
    def toggleLight(self):
        self.__light = not self.__light

        if self.__light:
            GPIO.output(PIN.RELAY4_LIGHT, GPIO.LOW)
            self.notify(MSG["light_on"])
        else:
            GPIO.output(PIN.RELAY4_LIGHT, GPIO.HIGH)
            self.notify(MSG["light_off"])

    def toggleSteam(self):
        self.__steam = not self.__steam

        if self.__steam:
            GPIO.output(PIN.RELAY5_STEAM, GPIO.LOW)
            self.notify(MSG["release_steam"])
        else:
            GPIO.output(PIN.RELAY5_STEAM, GPIO.HIGH)

    def toggleBurnerFan(self):
        self.__burnerFan = not self.__burnerFan

        if self.__burnerFan:
            GPIO.output(PIN.RELAY3_BURNER_FAN, GPIO.LOW)
            self.notify(MSG["fan_on"])
        else:
            GPIO.output(PIN.RELAY3_BURNER_FAN, GPIO.HIGH)
            self.notify(MSG["fan_off"])

    def toggleInternalOpening(self):
        self.manageIntOpeningButton(False)
        internalOpeningController = InternalOpeningController(controller = self)
        self.__threads.append(internalOpeningController)
        internalOpeningController.start()     

    def toggleExternalOpening(self):
        self.__externalOpening = not self.__externalOpening
        self.notify(MSG["ext_opening_triggered"])

        if self.__externalOpening:
            GPIO.output(PIN.RELAY7_EST_OPENING, GPIO.LOW)
        else:
            GPIO.output(PIN.RELAY7_EST_OPENING, GPIO.HIGH)
            
    def manageBurnerButtonAndLabel(self, state):
        self.__burner = state
        self.ui.manageBurnerSignal.emit(state)
        
    def isBurnerButtonEnabled(self):
        return self.ui.burnerButton.isEnabled()
    
    def toggleBurnerButtonEnabled(self, state):
        self.ui.burnerButton.setEnabled(state)

    def manageIntOpeningButton(self, state):
        self.ui.internalOpeningButton.setEnabled(state)

    def playAudio(self):
        # assumes that audio reproduction finishes before app exit
        subprocess.Popen(['mpg321', AUDIO_PATH])
        self.notifyCritical(MSG["timeout"])

    def setThermostatValue(self, value):
        if value is not None:
            self.__setPoint = value
            self.notify(MSG["set_point"])

    def notify(self, message, time = 3000):
        self.ui.notifySignal.emit(message, False, time)
        
    def notifyCritical(self, message, time = 0):
        self.ui.notifySignal.emit(message, True, time)

    def close(self):
        self.__burnerController.kill()
        self.__burnerController.resume()
        self.__sensReader.kill()
        self.__fanController.kill()

        for thread in self.__threads:
            thread.join()

        GPIO.cleanup()
