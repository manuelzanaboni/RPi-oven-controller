#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread, Condition
import RPi.GPIO as GPIO

import utils.default_gpio as PIN
from utils.messages import BURNER_CONTROLLER_MSGS as MSG

SLEEP_TIME = 3 # (seconds) overall sleep time
PRESSION_CHECK_SLEEP = 10 # (seconds) sleep time after burner startup

class BurnerController(Thread):
    def __init__(self, controller):
        super(BurnerController, self).__init__()
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
            self.turnBurnerOff()
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
        if not self.getBurnerState():
            GPIO.output(PIN.RELAY1_BURNER, GPIO.LOW)
        
    def turnBurnerOff(self):
        """
        Atomic burner shut-down
        """
        if self.getBurnerState():
            GPIO.output(PIN.RELAY1_BURNER, GPIO.HIGH)
        
    def checkPression(self):
        """
        This method checks if oven internal pression is increased after burner start-up.
        """
        if not self.controller.isBurnerButtonEnabled():
            self.controller.toggleBurnerButtonEnabled(True)
            
        if self.controller.getDeltaPression() < self.controller.config["inputPressionThreshold"]:
            self.controller.manageBurnerButtonAndLabel(False)
            self.controller.notifyCritical(MSG["blockage"])
            self.pause()
            
    def manageBurnerValve(self):
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
                    self.state.wait()  # Block execution until notified.
                    
            if not self.upperCheckState:
                self.mainCicle()    # Burner main working cicle
            else:
                self.upperCheck()   # Check whether burner should be turned ON
       
        
    def mainCicle(self):
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

                    if self.controller.config["checkPression"]:
                        self.controller.notify(MSG["burner_startup"], 5000)
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
                    self.turnBurnerOff()
                    self.controller.manageBurnerButtonAndLabel(False)
                    self.controller.notify(MSG["temp_reached"])
                    
                    """ Start checking for upper tempererature, proceed with self.upperCheck() """
                    self.upperCheckState = True
                        
        if not self.paused:
            """
            Sleep only if thread (self) is not paused.
            If thread is paused, skip sleeping to enable fast start-up.
            (this avoid the need to disable burner button, in order to prevent fault)
            """
            time.sleep(SLEEP_TIME)
            
    def upperCheck(self):        
        if self.controller.thermostatCalling():
            self.upperCheckState = False
            self.controller.manageBurnerButtonAndLabel(True)
            
        """ Here Condition has been used to enable 'wake up on wait' """
        with self.state:
            self.state.wait(self.controller.config["inputUpperCheckerTime"])
