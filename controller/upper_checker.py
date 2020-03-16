#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread
import RPi.GPIO as GPIO

import utils.default_gpio as PIN

SLEEP_INTERVAL = 5

class UpperChecker(Thread):
    def __init__(self, controller, burner_controller):
        super(UpperChecker, self).__init__()
        self.controller = controller
        self.burner_controller = burner_controller
        self.stop = False

    def kill(self):
        self.stop = True
        
    def run(self):
        while not self.stop:
            print("SLEEPING...")
            time.sleep(SLEEP_INTERVAL)
            
            if self.controller.getOvenTemp() < self.controller.getSetPoint():
                print("WAKING UP BURNER")
                self.burner_controller.resume()
                self.kill()
                self.controller.manageBurnerButtonAndLabel(True)
                
        print("DONE")


