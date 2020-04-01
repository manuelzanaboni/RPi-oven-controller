#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
import time
from threading import Thread

import MAX6675.MAX6675 as MAX6675
import Adafruit_BMP.BMP085 as BMP085
import utils.default_gpio as PIN
from utils.messages import SENS_READER_MSGS as MSG

SLEEP_TIME = 3

class SensReader(Thread):
    def __init__(self, controller):
        super(SensReader, self).__init__()
        self.controller = controller

        self.ovenThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS1, PIN.SO1)
        self.floorThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS2, PIN.SO2)
        self.pufferThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS3, PIN.SO3)
        self.fumesThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS4, PIN.SO4)
        self.pressionSensor = BMP085.BMP085(busnum=1)
        self.gasSensor = BMP085.BMP085(busnum=4)
        
        self.stop = False

    def kill(self):
        self.stop = True
        
    def calibratePressionSensors(self):
        
        sum = 0
        for i in range(10): 
            sum += self.pressionSensor.read_pressure()
            time.sleep(0.3)
        
        mean1 = sum // 10

        sum = 0
        for i in range(10): 
            sum += self.gasSensor.read_pressure()
            time.sleep(0.3)
        
        mean2 = sum // 10

        return mean1, mean2
        
    def isNaN(self, val):
        return val != val
    
    def run(self):
        """ calibrate sensors"""
        self.controller.notify(MSG["calibration"])
        mean1, mean2 = self.calibratePressionSensors()

        self.controller.notify(MSG["startup"])
        
        while not self.stop:
            """ get data """
            ovenTemp = self.ovenThermocouple.readTempC()
            floorTemp = self.floorThermocouple.readTempC()
            pufferTemp = self.pufferThermocouple.readTempC()
            fumesTemp = self.fumesThermocouple.readTempC()
            
            pression1 = self.pressionSensor.read_pressure()
            delta1 = pression1 - mean1
            
            pression2 = self.gasSensor.read_pressure()
            delta2 = pression2 - mean2

            """ display data """
            self.controller.setData(ovenTemp, floorTemp, pufferTemp, fumesTemp, delta1, delta2)

            """ persist data """
            if self.controller.config["persistData"]:
                try:
                    con = sqlite3.connect('oven.db')
                    with con:
                        cur = con.cursor()
                        
                        if not self.isNaN(ovenTemp):
                            cur.execute("INSERT INTO OvenTemperatures VALUES(datetime('now', 'localtime'), " + str(ovenTemp) + ")")
                            
                        if not self.isNaN(floorTemp):
                            cur.execute("INSERT INTO FloorTemperatures VALUES(datetime('now', 'localtime'), " + str(floorTemp) + ")")
                            
                        if not self.isNaN(pufferTemp):
                            cur.execute("INSERT INTO PufferTemperatures VALUES(datetime('now', 'localtime'), " + str(pufferTemp) + ")")
                            
                        if not self.isNaN(fumesTemp):
                            cur.execute("INSERT INTO FumesTemperatures VALUES(datetime('now', 'localtime'), " + str(fumesTemp) + ")")
                            
                        con.commit()
                    con.close()
                except:
                    print("Couldn't write on DB")
                    self.controller.notifyCritical(MSG["DB_error"])
                    
            time.sleep(SLEEP_TIME)
