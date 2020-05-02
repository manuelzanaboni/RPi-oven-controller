#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread, Condition
import RPi.GPIO as GPIO

import utils.default_gpio as PIN

class UpperCheckerResistance(Thread):
    def __init__(self, controller, resistance_controller):
        super(UpperCheckerResistance, self).__init__()
        self.controller = controller
        self.resistance_controller = resistance_controller
        
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
                self.resistance_controller.resume()
                self.controller.manageResistanceButton(True)
                self.pause()