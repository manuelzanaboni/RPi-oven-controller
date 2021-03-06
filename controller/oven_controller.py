#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import subprocess
from math import isnan

import utils.default_gpio as PIN
from utils.messages import OVEN_CONTROLLER_MSGS as MSG
from .burner_controller import BurnerController
from .resistance_controller import ResistanceController
from .sens_reader import SensReader
from .rpi_fan import FanController
from .internal_opening_controller import InternalOpeningController

AUDIO_PATH = 'resources/audio.mp3' # where to find audio file to be played
UPPER_SAFETY_PRESSION_THRESHOLD = 500 # (Pa) delta pression threshold. if greater, burner must turn off.

class OvenController(object):
    def __init__(self, ui, config):
        self.ui = ui
        self.config = config
        
        self.__ovenTemp = 0 # holds oven internal temperature
        self.__floorTemp = 0 # holds oven's floor temperature
        self.__pufferTemp = 0 # holds puffer temperature (water)
        self.__fumesTemp = 0 # holds exhaust fumes temperture
        self.__deltaPression = 0 # holds pression variation
        self.__deltaGas = 0 # holds gas pression variation
        
        self.__setPoint = self.ui.horizontalSlider.value() # system set point

        """ state variables """
        self.__burner = False
        self.__burnerValve = False
        self.__overrideValve = None
        self.__light = False
        self.__steam = False
        self.__burnerFan = False
        self.__externalOpening = False
        self.__rotisserie = False
        self.__resistance = False
        self.__vacuum = False
        self.__realTime = False

        """ initialize Relay GPIO """
        GPIO.setmode(GPIO.BCM)
        gpioList = [PIN.RELAY1_BURNER, PIN.RELAY2_BURNER_VALVE, PIN.RELAY3_BURNER_FAN,
                    PIN.RELAY4_LIGHT, PIN.RELAY5_STEAM, PIN.RELAY6_INT_OPENING,
                    PIN.RELAY7_EST_OPENING, PIN.RELAY8_RPI_FAN, PIN.RELAY9_ROTISSERIE,
                    PIN.RELAY10_RESISTANCE, PIN.RELAY11_VACUUM, PIN.RELAY12_UNUSED]

        for i in gpioList:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

        """ threads """
        self.__threads = []

        self.__burnerController = BurnerController(controller = self)
        self.__threads.append(self.__burnerController)
        self.__burnerController.start()
        
        self.__resistanceController = ResistanceController(controller = self)
        self.__threads.append(self.__resistanceController)
        self.__resistanceController.start()
            
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
    
    def getOverrideValve(self):
        return self.__overrideValve
    
    def getLowerThermostatBound(self):
        return self.ui.horizontalSlider.minimum()

    def setData(self, ovenTemp, floorTemp, pufferTemp, fumesTemp, deltaPression, deltaGas):
        if ovenTemp is not None and not isnan(ovenTemp):
            self.__ovenTemp = ovenTemp
            self.ui.ovenLCD.display(self.__ovenTemp)
        else:
            self.__ovenTemp = 0
            self.ui.ovenLCD.display("---")

        if floorTemp is not None and not isnan(floorTemp):
            self.__floorTemp = floorTemp
            self.ui.floorLCD.display(self.__floorTemp)
        else:
            self.__floorTemp = 0
            self.ui.floorLCD.display("---")

        if pufferTemp is not None and not isnan(pufferTemp):
            self.__pufferTemp = pufferTemp
            self.ui.pufferLCD.display(self.__pufferTemp)
        else:
            self.__pufferTemp = 0
            self.ui.pufferLCD.display("---")

        if fumesTemp is not None and not isnan(fumesTemp):
            self.__fumesTemp = fumesTemp
            self.ui.fumesLCD.display(self.__fumesTemp)
        else:
            self.__fumesTemp = 0
            self.ui.fumesLCD.display("---")

        if deltaPression is not None and not isnan(deltaPression):
            self.__deltaPression = deltaPression
            self.ui.pressionLCD.display(self.__deltaPression)
            
            if self.__burner and self.__deltaPression >= UPPER_SAFETY_PRESSION_THRESHOLD: # react to possible blockage
                self.notifyCritical(MSG["burner_blockage"])
                self.manageBurnerButtonAndLabel(False)
                self.__burnerController.pause()
        else:
            self.__deltaPression = 0
            self.ui.pressionLCD.display("----")
            
        if deltaGas is not None and not isnan(deltaGas):
            self.__deltaGas = deltaGas
            self.ui.gasLCD.display(self.__deltaGas)
        else:
            self.__deltaGas = 0
            self.ui.gasLCD.display("----")
        
        """ Send data to charts if real time is enabled """
        if self.__realTime:
            self.ui.chartsController.updateChartRealTime(ovenTemp, floorTemp, pufferTemp, fumesTemp)
            
    def setConfig(self, config):
        self.config = config

    def setRealTime(self, state):
        self.__realTime = state
    
    def toggleBurner(self):
        """ Turn OFF steam and burner Fan if active, before starting burner """
        if not self.__burner and self.__steam:
            self.toggleSteam()
            
        if not self.__burner and self.__burnerFan:
            self.ui.toggleFan()
        
        """ Manage burner """
        self.__burner = not self.__burner
        
        if self.thermostatCalling():
            if self.__burner:
                """ Turn Burner ON """
                self.__burnerController.resume()
                return True
            else:
                """ Turn burner OFF """
                self.__burnerController.pause()
                return False
        else:
            if self.__burner:
                """ Stop burner cicle """
                self.notify(MSG["burner_off_upper"])
                self.__burner = False
                self.__burnerController.setUpperCheckState(False)
                self.__burnerController.upperPause()
                return None
            
    def toggleBurnerValve(self):
        self.__burnerValve = not self.__burnerValve
        
        if self.__burnerValve:
            self.__overrideValve = True
            self.openValve()
        else:
            self.__overrideValve = False
            self.closeValve()
            
    def openValve(self, thermostatOverride = None):
        
        if thermostatOverride is not None:
            self.__burnerValve = thermostatOverride
            self.ui.burnerValveButton.setChecked(thermostatOverride)
            #self.ui.manageValveLabel(state = self.__burnerValve)
            self.ui.manageValveSignal.emit(self.__burnerValve)
            
        GPIO.output(PIN.RELAY2_BURNER_VALVE, GPIO.LOW)
        self.notify(MSG["valve_on"])
        
    def closeValve(self, thermostatOverride = None):
        
        if thermostatOverride is not None:
            self.__burnerValve = thermostatOverride
            self.ui.burnerValveButton.setChecked(thermostatOverride)
            #self.ui.manageValveLabel(state = self.__burnerValve)
            self.ui.manageValveSignal.emit(self.__burnerValve)
            
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
        if not self.__burner: 
            self.__steam = not self.__steam

            if self.__steam:
                GPIO.output(PIN.RELAY5_STEAM, GPIO.LOW)
                self.notify(MSG["release_steam"])
            else:
                GPIO.output(PIN.RELAY5_STEAM, GPIO.HIGH)
        else:
            self.notifyCritical(MSG["function_disabled"])

    def toggleBurnerFan(self):
        if not self.__burner:
            self.__burnerFan = not self.__burnerFan

            if self.__burnerFan:
                GPIO.output(PIN.RELAY3_BURNER_FAN, GPIO.LOW)
                self.notify(MSG["fan_on"])
            else:
                GPIO.output(PIN.RELAY3_BURNER_FAN, GPIO.HIGH)
                self.notify(MSG["fan_off"])
                
            return True
        else:
            self.notifyCritical(MSG["function_disabled"])
            return False

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
            
    def toggleRotisserie(self):
        self.__rotisserie = not self.__rotisserie

        if self.__rotisserie:
            GPIO.output(PIN.RELAY9_ROTISSERIE, GPIO.LOW)
            #self.notify(MSG["light_on"])
        else:
            GPIO.output(PIN.RELAY9_ROTISSERIE, GPIO.HIGH)
            #self.notify(MSG["light_off"])
            
    def toggleResistance(self):
        self.__resistance = not self.__resistance            
            
        if self.thermostatCalling():
            if self.__resistance:
                """ Turn Resistance ON """
                self.__resistanceController.resume()
                return True
            else:
                """ Turn Resistance OFF """
                self.__resistanceController.pause()
                return False
        else:
            if self.__resistance:
                """ Stop Resistance cicle """
                self.notify(MSG["resistance_off_upper"])
                self.__resistance = False
                self.__resistanceController.setUpperCheckState(False)
                self.__resistanceController.upperPause()
                return None
            
    def toggleVacuum(self):
        self.__vacuum = not self.__vacuum

        if self.__vacuum:
            GPIO.output(PIN.RELAY11_VACUUM, GPIO.LOW)
            #self.notify(MSG["light_on"])
        else:
            GPIO.output(PIN.RELAY11_VACUUM, GPIO.HIGH)
            #self.notify(MSG["light_off"])
            
    def thermostatCalling(self):
        """
        Whether the burner should be ON or OFF.
        Returns True if SetPoint is greater than current internal temperature
        """
        return self.getSetPoint() > self.getOvenTemp()
                        
    def manageBurnerButtonAndLabel(self, state):
        if state is not None:
            self.__burner = state
            self.ui.manageBurnerSignal.emit(state)
        
    def manageResistanceLabel(self, state):
        if state is not None:
            self.__resistance = state
            self.ui.manageResistanceSignal.emit(state)
        
    def isBurnerButtonEnabled(self):
        return self.ui.burnerButton.isEnabled()
    
    def toggleBurnerButtonEnabled(self, state):
        self.ui.burnerButton.setEnabled(state)

    def manageIntOpeningButton(self, state):
        self.ui.internalOpeningButton.setEnabled(state)

    def playAudio(self):
        # assumes that audio playback finishes before app exit
        subprocess.Popen(['mpg321', AUDIO_PATH])
        self.notifyCritical(MSG["timeout"])

    def setThermostatValue(self, value):
        if value is not None:
            self.__setPoint = value
            self.notify(MSG["set_point"])
            
    def calibratePressionSensors(self):
        self.__sensReader.setReCalibrate(True)

    def notify(self, message, time = 3000):
        self.ui.notifySignal.emit(message, False, time)
        
    def notifyCritical(self, message, time = 0):
        self.ui.notifySignal.emit(message, True, time)

    def close(self):
        self.__burnerController.kill()
        self.__resistanceController.kill()        
        self.__sensReader.kill()
        self.__fanController.kill()

        for thread in self.__threads:
            thread.join()

        GPIO.cleanup()
