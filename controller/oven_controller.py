#!/usr/bin/python3
# coding: utf8

# import RPi.GPIO as GPIO
from .sens_reader import SensReader

class OvenController(object):
    def __init__(self, ui):
        self.ui = ui

        self.__ovenTemp = 0
        self.__floorTemp = 0
        self.__pufferTemp = 0
        self.__fumesTemp = 0

        # initialize Relay GPIO
        # GPIO.setmode(GPIO.BCM)
        # gpioList = [4, 17, 18, 27, 22, 23, 24, 25]
        # for i in gpioList:
        #     GPIO.setup(i, GPIO.OUT)
        #     GPIO.output(i, GPIO.HIGH)

        #definire Pool
        self.sensReader = SensReader(controller = self)
        self.sensReader.daemon = True
        self.sensReader.start()

    def getOvenTemp(self):
        return self.__ovenTemp

    def setData(self, ovenTemp, floorTemp, pufferTemp, fumesTemp):  #add feedback on failure?
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

