#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread
import default_gpio as PIN
import RPi.GPIO as GPIO

SLEEP_INTERVAL = 5

class InternalOpeningController(Thread):
    def __init__(self, controller):
        super(InternalOpeningController, self).__init__()
        self.controller = controller
        self.stop = False

    def kill(self):
        self.stop = True
        
    def run(self):
        self.controller.notify("Apertura interna azionata.", 3000)
        GPIO.output(PIN.RELAY6_INT_OPENING, GPIO.LOW)
        time.sleep(SLEEP_INTERVAL)
        GPIO.output(PIN.RELAY6_INT_OPENING, GPIO.HIGH)
        self.controller.manageIntOpeningButton(True)
