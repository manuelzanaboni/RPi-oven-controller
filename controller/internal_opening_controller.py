#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread
import RPi.GPIO as GPIO

import utils.default_gpio as PIN
from utils.messages import INTERNAL_OPENING_MSGS as MSG

SLEEP_INTERVAL = 5

class InternalOpeningController(Thread):
    def __init__(self, controller):
        super(InternalOpeningController, self).__init__()
        self.controller = controller
        self.stop = False

    def kill(self):
        self.stop = True
        
    def run(self):
        self.controller.notify(MSG["opening_triggered"])
        GPIO.output(PIN.RELAY6_INT_OPENING, GPIO.LOW)
        time.sleep(SLEEP_INTERVAL)
        GPIO.output(PIN.RELAY6_INT_OPENING, GPIO.HIGH)
        self.controller.manageIntOpeningButton(True)
