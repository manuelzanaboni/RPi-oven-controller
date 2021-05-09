#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from threading import Thread
import RPi.GPIO as GPIO
import subprocess

from datetime import datetime

import utils.default_gpio as PIN

ON_THRESHOLD = 45  # (degrees Celsius) Fan kicks on at this temperature.
OFF_THRESHOLD = 39  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.

class FanController(Thread):
    def __init__(self, controller):
        super(FanController, self).__init__()
        self.controller = controller
        self.stop = False

    def kill(self):
        self.stop = True
    
    def getTemp(self):
        """Get the core temperature.
        Run a shell script to get the core temperature and parse the output.
        Raises:
            RuntimeError: if response cannot be parsed.
        Returns:
            float: The core temperature in degrees Celsius.
        """
        output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
        temp_str = output.stdout.decode()
        try:
            return float(temp_str.split('=')[1].split('\'')[0])
        except (IndexError, ValueError):
            raise RuntimeError('Could not parse temperature output.')
        
    def run(self):
        while not self.stop:
            temp = self.getTemp()
            t = datetime.now().strftime("%H:%M:%S")
            
            print(t, " T: ", str(temp))
            
            pinState = GPIO.input(PIN.RELAY8_RPI_FAN)

            if temp > ON_THRESHOLD and pinState:
                GPIO.output(PIN.RELAY8_RPI_FAN, GPIO.LOW)
            elif not pinState and temp < OFF_THRESHOLD:
                GPIO.output(PIN.RELAY8_RPI_FAN, GPIO.HIGH)
                
            time.sleep(SLEEP_INTERVAL)