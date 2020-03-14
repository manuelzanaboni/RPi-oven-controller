#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread, Condition
import RPi.GPIO as GPIO

import utils.default_gpio as PIN
from utils.messages import BURNER_CONTROLLER_MSGS as MSG

SLEEP_TIME = 3 # (seconds) overall sleep time
PRESSION_CHECK_SLEEP = 10 # (seconds) sleep time after burner startup
PRESSION_DELTA_THRESHOLD = 30 # (Pa) minimum delta pression that the burner should generate
TEMP_DELTA_TO_REACH_SETPOINT = 30 # (degress Celsius) setpoint valve fallback

class BurnerController(Thread):
    def __init__(self, controller):
        super(BurnerController, self).__init__()
        self.controller = controller
        self.paused = True # Start out paused.
        self.state = Condition()        
        self.stop = False
        
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
        
    def thermostatCalling(self):
        """
        Whether the burner should be ON or OFF.
        Returns True if SetPoint is greater than current internal temperature
        """
        return self.controller.getSetPoint() > self.controller.getOvenTemp()
    
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
        if self.controller.getDeltaPression() < PRESSION_DELTA_THRESHOLD:
            self.controller.manageBurnerButtonAndLabel(False)
            self.pause()
            self.controller.notifyCritical(MSG["blockage"])
            
        if not self.controller.isBurnerButtonEnabled():
            self.controller.toggleBurnerButtonEnabled(True)
            
    def manageBurnerValve(self): #TODO
        """
        Stage1 - setPoint >= 150, t = 100 apri valvola
        Stage2 - setPoint - 30 chiudi valvola
        """
        ovenTemp = self.controller.getOvenTemp()
        lowerBound = self.controller.getLowerThermostatBound()
        setPoint = self.controller.getSetPoint()
        valveState = self.controller.getBurnerValve()
        
        """
        Al momento
        apre a 100 gradi, chiude a setpoint - 30
        setpoint tra 100 e 129 non apre
        setpoint 130 apre...al ciclo dopo chiude
        setpoint alto...tutto ok
        """
        if ovenTemp >= lowerBound and ovenTemp <= (setPoint - TEMP_DELTA_TO_REACH_SETPOINT):
            if not valveState:
                self.controller.toggleBurnerValve(thermostatOverride = True)
        else:
            if valveState:
                self.controller.toggleBurnerValve(thermostatOverride = False)
        
    def run(self):
        while not self.stop:                    
            with self.state:
                if self.paused:
                    print("Thread paused, waiting to resume...")
                    self.state.wait()  # Block execution until notified.
            
            if not self.stop: # skip execution if kill() has been called
                
                if self.thermostatCalling():
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
                        self.controller.toggleBurnerButtonEnabled(False)
                        self.controller.notify(MSG["burner_startup"], 5000)
                        
                        time.sleep(PRESSION_CHECK_SLEEP)
                        
                        self.checkPression()
                    else:
                        """
                        Burner is already ON.
                        Keep checking pression.
                        Open/Close burner valve according to operating curve.
                        """
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
            
            if not self.paused:
                """
                Sleep only if thread (self) is not paused.
                If thread is paused, skip sleeping to enable fast start-up.
                (this avoid the need to disable burner button, in order to prevent fault)
                """
                time.sleep(SLEEP_TIME)
            
        print("Stopping thread")