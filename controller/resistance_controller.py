#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread, Condition
import RPi.GPIO as GPIO

import utils.default_gpio as PIN
from utils.messages import RESISTANCE_CONTROLLER_MSGS as MSG
from .upper_checker_resistance import UpperCheckerResistance

SLEEP_TIME = 3 # (seconds) overall sleep time

class ResistanceController(Thread):
    def __init__(self, controller):
        super(ResistanceController, self).__init__()
        self.controller = controller
        self.paused = True # Start out paused.
        self.state = Condition()        
        self.stop = False
        
        self.upperChecker = UpperCheckerResistance(controller = self.controller, resistance_controller = self)
        self.upperChecker.start()
        
    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify() # Execute self if waiting.
            
    def pause(self):
        if not self.paused:
            self.turnResistanceOff()
            with self.state:
                self.paused = True # Pause self.
            
    def kill(self):
        """
        End self execution.
        Method called on application exit.
        """
        self.stop = True
        if self.paused:
            self.resume()   
        
    def getResistanceState(self):
        """
        Returns resistance state (True or False):
        GPIO.HIGH = 1 --> Resistance OFF --> return False
        GPIO.LOW = 0 --> Resistance ON --> return True
        """
        return not GPIO.input(PIN.RELAY10_RESISTANCE)
    
    def turnResistanceOn(self):
        """
        Atomic resistance start-up
        """
        GPIO.output(PIN.RELAY10_RESISTANCE, GPIO.LOW)
        
    def turnResistanceOff(self):
        """
        Atomic resistance shut-down
        """
        GPIO.output(PIN.RELAY10_RESISTANCE, GPIO.HIGH)
        
    def run(self):
        while not self.stop:                    
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            
            if not self.stop: # skip execution if kill() has been called
                
                if self.controller.thermostatCalling():
                    """
                    Here thermostat is triggered, thus resistance should be ON.
                    """
                    if not self.getResistanceState():
                        """
                        Resistance is currently OFF --> startup.
                        """
                        self.turnResistanceOn()                        
                else:
                    """
                    Here thermostat is not triggered, thus resistance should be OFF.
                    """                    
                    if self.getResistanceState():
                        self.pause()
                        self.controller.manageResistanceButton(False)
                        self.controller.notify(MSG["temp_reached"])
                        
                        """ Start checking for upper tempererature """
                        self.upperChecker.resume()
            
            if not self.paused:
                """
                Sleep only if thread (self) is not paused.
                """
                time.sleep(SLEEP_TIME)
                
             
        if self.upperChecker.isAlive():
            self.upperChecker.kill()
            
        self.upperChecker.join()