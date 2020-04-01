#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread, Condition
import RPi.GPIO as GPIO

import utils.default_gpio as PIN
from utils.messages import BURNER_CONTROLLER_MSGS as MSG
from .upper_checker import UpperChecker

SLEEP_TIME = 3 # (seconds) overall sleep time
PRESSION_CHECK_SLEEP = 10 # (seconds) sleep time after burner startup

class BurnerController(Thread):
    def __init__(self, controller):
        super(BurnerController, self).__init__()
        self.controller = controller
        self.paused = True # Start out paused.
        self.state = Condition()        
        self.stop = False
        
        self.upperChecker = UpperChecker(controller = self.controller, burner_controller = self)
        self.upperChecker.start()
        
    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify() # Execute self if waiting.
            
    def pause(self):
        if not self.paused:
            self.turnBurnerOff()
            with self.state:
                self.paused = True # Pause self.
            
    def kill(self):
        """
        End self execution.
        Method called on application exit.
        """
        self.stop = True
    
    def getBurnerState(self):
        """
        Returns burner state (True or False):
        GPIO.HIGH = 1 --> Burner OFF --> return False
        GPIO.LOW = 0 --> Burner ON --> return True
        """
        return not GPIO.input(PIN.RELAY1_BURNER)
    
    def turnBurnerOn(self):
        """
        Atomic burner start-up
        """
        GPIO.output(PIN.RELAY1_BURNER, GPIO.LOW)
        
    def turnBurnerOff(self):
        """
        Atomic burner shut-down
        """
        GPIO.output(PIN.RELAY1_BURNER, GPIO.HIGH)
        
    def checkPression(self):
        """
        This method checks if oven internal pression is increased after burner start-up.
        """            
        if self.controller.getDeltaPression() < self.controller.config["inputPressionThreshold"]:
            self.controller.manageBurnerButtonAndLabel(False)
            self.pause()
            self.controller.notifyCritical(MSG["blockage"])
            
        if not self.controller.isBurnerButtonEnabled():
            self.controller.toggleBurnerButtonEnabled(True)
            
    def manageBurnerValve(self): #TODO

        ovenTemp = self.controller.getOvenTemp()
        lowerBound = self.controller.getLowerThermostatBound()
        setPoint = self.controller.getSetPoint()
        valveState = self.controller.getBurnerValve()
        delta = self.controller.config["inputValveThreshold"]
        
        if ovenTemp >= lowerBound and ovenTemp <= (setPoint - delta):
            if not valveState:
                self.controller.openValve(thermostatOverride = True)
        else:
            if not self.controller.getOverrideValve() and valveState:
                self.controller.closeValve(thermostatOverride = False)
        
    def run(self):
        while not self.stop:                    
            with self.state:
                if self.paused:
                    print("Thread paused, waiting to resume...")
                    self.state.wait()  # Block execution until notified.
            
            #print("executing")
            
            if not self.stop: # skip execution if kill() has been called
                
                if self.controller.thermostatCalling():
                    """
                    Here thermostat is triggered, thus burner should be ON.
                    """
                    if not self.getBurnerState():
                        """
                        Burner is currently OFF --> startup.
                        Disable burner button to prevent faults.
                        Check if pression is raised after burner startup.
                        """
                        self.turnBurnerOn()

                        self.controller.notify(MSG["burner_startup"], 5000)
                        
                        if self.controller.config["checkPression"]:
                            self.controller.toggleBurnerButtonEnabled(False)
                            time.sleep(PRESSION_CHECK_SLEEP)
                            self.checkPression()
                    else:
                        """
                        Burner is already ON.
                        Keep checking pression.
                        Open/Close burner valve according to operating curve.
                        """
                        if self.controller.config["checkPression"]:
                            self.checkPression()

                        self.manageBurnerValve()
                        
                else:
                    """
                    Here thermostat is not triggered, thus burner should be OFF.
                    """                    
                    if self.getBurnerState():
                        self.pause()
                        self.controller.manageBurnerButtonAndLabel(False)
                        self.controller.notify(MSG["temp_reached"])
                        
                        """ Start checking for upper tempererature """
                        self.upperChecker.resume()
            
            if not self.paused:
                """
                Sleep only if thread (self) is not paused.
                If thread is paused, skip sleeping to enable fast start-up.
                (this avoid the need to disable burner button, in order to prevent fault)
                """
                time.sleep(SLEEP_TIME)
                
                
        if self.upperChecker.isAlive():
            self.upperChecker.kill()
            
        self.upperChecker.join()