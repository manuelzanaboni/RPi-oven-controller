#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import default_gpio as PIN
import subprocess

from .sens_reader import SensReader
from .rpi_fan import FanController
from .internal_opening_controller import InternalOpeningController

AUDIO_PATH = 'src/audio.mp3'

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

        self.__sensReader = SensReader(controller = self)
        self.__sensReader.start()
        self.__threads.append(self.__sensReader)

        self.__fanController = FanController(controller = self)
        self.__fanController.start()
        self.__threads.append(self.__fanController)

    def getOvenTemp(self):
        return self.__ovenTemp

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
            self.ui.pressureLCD.display(self.__deltaPression)

    def toggleLight(self):
        self.__light = not self.__light

        if self.__light:
            GPIO.output(PIN.RELAY4_LIGHT, GPIO.LOW)
            self.notify("Accensione luce.", 3000)
        else:
            GPIO.output(PIN.RELAY4_LIGHT, GPIO.HIGH)
            self.notify("Spegnimento luce.", 3000)


    def toggleSteam(self):
        self.__steam = not self.__steam

        if self.__steam:
            GPIO.output(PIN.RELAY5_STEAM, GPIO.LOW)
            self.notify("Rilascio vapore.", 2000)
        else:
            GPIO.output(PIN.RELAY5_STEAM, GPIO.HIGH)

    def toggleBurnerFan(self):
        self.__burnerFan = not self.__burnerFan

        if self.__burnerFan:
            GPIO.output(PIN.RELAY3_BURNER_FAN, GPIO.LOW)
            self.notify("Ventola bruciatore attivata.", 3000)
        else:
            GPIO.output(PIN.RELAY3_BURNER_FAN, GPIO.HIGH)
            self.notify("Ventola bruciatore disattivata.", 3000)

    def toggleInternalOpening(self):
        self.manageIntOpeningButton(False)
        internalOpeningController = InternalOpeningController(self)
        internalOpeningController.start()
        self.__threads.append(internalOpeningController)

    def toggleExternalOpening(self):
        self.__externalOpening = not self.__externalOpening
        self.notify("Apertura esterna azionata.", 3000)

        if self.__externalOpening:
            GPIO.output(PIN.RELAY7_EST_OPENING, GPIO.LOW)
        else:
            GPIO.output(PIN.RELAY7_EST_OPENING, GPIO.HIGH)

    def manageIntOpeningButton(self, state):
        self.ui.internalOpeningButton.setEnabled(state)

    def playAudio(self):
        # assumes that audio reproduction finishes before app exit
        subprocess.Popen(['mpg321', AUDIO_PATH])
        self.notify("Timer scattato!!", 5000)

    def setThermostatValue(self, value): # TODO
        self.notify("Nuova temperatura impostata.", 3000)

    def notify(self, message, time):
        self.ui.notifySignal.emit(message, time)

    def close(self):
        self.__sensReader.kill()
        self.__fanController.kill()

        for thread in self.__threads:
            thread.join()

        GPIO.cleanup()
