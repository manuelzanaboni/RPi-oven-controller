#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread, Condition
import RPi.GPIO as GPIO

import utils.default_gpio as PIN
from utils.messages import BURNER_CONTROLLER_MSGS as MSG

SLEEP_TIME = 3
PRESSION_DELTA_THRESHOLD = 30

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
        self.stop = True
        
    def thermostatCalling(self):
        """
        Wheter the burner should be ON or OFF.
        Returns True if SetPoint is greater than current internal temperature
        """
        return self.controller.getSetPoint() > self.controller.getOvenTemp()
    
    def getBurnerRelayState(self):
        """
        Returns burner relay state (0 or 1):
        1 = GPIO.HIGH = Burner OFF
        0 = GPIO.LOW = Burner ON
        """
        return GPIO.input(PIN.RELAY1_BURNER)
    
    def turnBurnerOn(self):
        GPIO.output(PIN.RELAY1_BURNER, GPIO.LOW)
        
    def turnBurnerOff(self):
        GPIO.output(PIN.RELAY1_BURNER, GPIO.HIGH)
        
    def checkPression(self):
        print("Waiting to check pression increment...")
        self.controller.toggleBurnerButtonEnabled(True)
        if self.controller.getDeltaPression() > PRESSION_DELTA_THRESHOLD:
            print("Everything is fine!")
        else:
            print("Burner started but pression didnt't increase!")
            print("Stopping Burner and pausing thread")
            self.controller.manageBurnerButtonAndLabel(False)
            self.pause()
            
    def setBurnerStage(self): #TODO
        """
        Stage1 - setPoint >= 150, t = 100 apri valvola
        Stage2 - setPoint - 30 chiudi valvola
        """
        pass
        
    def run(self):
        while not self.stop:
            with self.state:
                if self.paused:
                    print("Thread paused, waiting to resume...")
                    self.state.wait()  # Block execution until notified.
                    
            print("Executing")
            if not self.stop: # skip execution if kill() has been called
                
                if self.thermostatCalling():
                    print("Burner should be ON")
                    print("Relay is: " + str(self.getBurnerRelayState()))
                    
                    if self.getBurnerRelayState():
                        # burner start-up and pression check
                        self.turnBurnerOn()
                        self.controller.toggleBurnerButtonEnabled(False)
                        print("Now Relay is: " + str(self.getBurnerRelayState()))
                        
                        time.sleep(10)
                        self.checkPression()
                    else:
                        # burner staging
                        self.checkPression()
                        print("Thermostat calling, burner already ON")
                        self.setBurnerStage() # TODO
                            
                else:
                    print("Burner should be OFF")
                    print("Relay is: " + str(self.getBurnerRelayState()))
                    
                    # TODO RESET STAGING
                    
                    if not self.getBurnerRelayState():
                        self.controller.manageBurnerButtonAndLabel(False)
                        self.pause()
                        print("Now Relay is: " + str(self.getBurnerRelayState()))
                
            
            if not self.stop:
                time.sleep(SLEEP_TIME)
            
        print("Stopping thread")
            
            
            
            
