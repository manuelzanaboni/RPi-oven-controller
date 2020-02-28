#!/usr/bin/python3
# coding: utf8

import RPi.GPIO as GPIO
from .sens_reader import SensReader
import default_gpio as PIN

class OvenController(object):
    def __init__(self, ui):
        self.ui = ui

        self.__ovenTemp = 0
        self.__floorTemp = 0
        self.__pufferTemp = 0
        self.__fumesTemp = 0
        self.__deltaPression = 0
        
        self.__light = False
        self.__steam = False
        self.__burnerFan = False
        self.__internalOpening = False
        self.__externalOpening = False

        # initialize Relay GPIO
        GPIO.setmode(GPIO.BCM)
        gpioList = [PIN.RELAY1_BURNER, PIN.RELAY2_BURNER_VALVE, PIN.RELAY3_BURNER_FAN,
                    PIN.RELAY4_LIGHT, PIN.RELAY5_STEAM, PIN.RELAY6_INT_OPENING,
                    PIN.RELAY7_EST_OPENING, PIN.RELAY8_RPI_FAN]
        for i in gpioList:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

        #definire Pool
        self.sensReader = SensReader(controller = self)
        #self.sensReader.daemon = True
        self.sensReader.start()

    def getOvenTemp(self):
        return self.__ovenTemp

    def setData(self, ovenTemp, floorTemp, pufferTemp, fumesTemp, deltaPression):  #add feedback on failure?
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
            self.ui.pressureLCD.display(self.__deltaPression)
            
    def toggleLight(self):
        self.__light = not self.__light
        
        if self.__light:
            GPIO.output(PIN.RELAY4_LIGHT, GPIO.LOW)
        else:
            GPIO.output(PIN.RELAY4_LIGHT, GPIO.HIGH)
            
            
    def toggleSteam(self):
        self.__steam = not self.__steam
        
        if self.__steam:
            GPIO.output(PIN.RELAY5_STEAM, GPIO.LOW)
        else:
            GPIO.output(PIN.RELAY5_STEAM, GPIO.HIGH)
            
    def toggleBurnerFan(self):
        self.__burnerFan = not self.__burnerFan
        
        if self.__burnerFan:
            GPIO.output(PIN.RELAY3_BURNER_FAN, GPIO.LOW)
        else:
            GPIO.output(PIN.RELAY3_BURNER_FAN, GPIO.HIGH)
            
    def toggleInternalOpening(self):
        self.__internalOpening = not self.__internalOpening
        
        if self.__internalOpening:
            GPIO.output(PIN.RELAY6_INT_OPENING, GPIO.LOW)
        else:
            GPIO.output(PIN.RELAY6_INT_OPENING, GPIO.HIGH)
    
    def toggleExternalOpening(self):
        self.__externalOpening = not self.__externalOpening
        
        if self.__externalOpening:
            GPIO.output(PIN.RELAY7_EST_OPENING, GPIO.LOW)
        else:
            GPIO.output(PIN.RELAY7_EST_OPENING, GPIO.HIGH)
            
    def notify(self, message):
        self.ui.notify(message)
        
    def close(self):
        self.sensReader.kill()
        GPIO.cleanup()

