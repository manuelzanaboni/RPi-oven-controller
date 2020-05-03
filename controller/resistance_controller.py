#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread, Condition
import RPi.GPIO as GPIO

import utils.default_gpio as PIN
from utils.messages import RESISTANCE_CONTROLLER_MSGS as MSG

SLEEP_TIME = 3 # (seconds) overall sleep time

class ResistanceController(Thread):
    def __init__(self, controller):
        super(ResistanceController, self).__init__()
        self.controller = controller
        self.paused = True # Start out paused.     
        self.stop = False
        
        self.state = Condition()   
        
        self.upperCheckState = False
        
    def setUpperCheckState(self, state):
        if state is not None:
            self.upperCheckState = state
            
    def resume(self):
        self.paused = False
        
        with self.state:  
            self.state.notify() # Execute self if waiting.
            
    def pause(self):
        if not self.paused:
            self.turnResistanceOff()
            self.paused = True # Pause self.
            
    def upperPause(self):
        """
        This method is used to manage user's input to turn burner OFF,
        when this thread is waiting (Condition) in upperCheck() method.
        Basically, this reset wait timeout.
        """
        self.paused = True
        with self.state:
            self.state.notify()
            
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
        if not self.getResistanceState():
            GPIO.output(PIN.RELAY10_RESISTANCE, GPIO.LOW)
        
    def turnResistanceOff(self):
        """
        Atomic resistance shut-down
        """
        if self.getResistanceState():
            GPIO.output(PIN.RELAY10_RESISTANCE, GPIO.HIGH)
        
    def run(self):
        while not self.stop:
            
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
                    
            if not self.upperCheckState:
                self.mainCicle()    # Burner main working cicle
            else:
                self.upperCheck()   # Check whether burner should be turned ON
        
    def mainCicle(self):
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
                    self.turnResistanceOff()
                    self.controller.manageResistanceLabel(False)
                    self.controller.notify(MSG["temp_reached"])
                    
                    """ Start checking for upper tempererature, proceed with self.upperCheck() """
                    self.upperCheckState = True
        
        if not self.paused:
            """
            Sleep only if thread (self) is not paused.
            """
            time.sleep(SLEEP_TIME)
            
    def upperCheck(self):        
        if self.controller.thermostatCalling():
            self.upperCheckState = False
            self.controller.manageResistanceLabel(True)
            
        """ Here Condition has been used to enable 'wake up on wait' """
        with self.state:
            self.state.wait(self.controller.config["inputUpperCheckerTime"])

