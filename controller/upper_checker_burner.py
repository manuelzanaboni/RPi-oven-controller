#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread, Condition
import RPi.GPIO as GPIO

import utils.default_gpio as PIN

class UpperCheckerBurner(Thread):
    def __init__(self, controller, burner_controller):
        super(UpperCheckerBurner, self).__init__()
        self.controller = controller
        self.burner_controller = burner_controller
        
        self.paused = False
        self.state = Condition()
        
        self.stop = False

    def resume(self):
        if self.paused:
            with self.state:
                self.paused = False
                self.state.notify() # Execute self if waiting.
            
    def pause(self):
        if not self.paused:
            with self.state:
                self.paused = True # Pause self.
                self.state.wait()
                
    def kill(self):
        self.stop = True
        if self.paused:
            self.resume()     
        
    def run(self):
        self.pause()
        
        while not self.stop:
            time.sleep(self.controller.config["inputUpperCheckerTime"])
            
            if self.controller.thermostatCalling():
                self.burner_controller.resume()
                self.controller.manageBurnerButtonAndLabel(True)
                self.pause()


