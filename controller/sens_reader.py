#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
import time
from threading import Thread
from math import isnan

import MAX6675.MAX6675 as MAX6675
import Adafruit_BMP.BMP085 as BMP085
import utils.default_gpio as PIN
from utils.messages import SENS_READER_MSGS as MSG

SLEEP_TIME = 3

class SensReader(Thread):
    def __init__(self, controller):
        super(SensReader, self).__init__()
        
        self.controller = controller
        """ Sensors initialization """
        self.ovenThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS1, PIN.SO1)
        self.floorThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS2, PIN.SO2)
        self.pufferThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS3, PIN.SO3)
        self.fumesThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS4, PIN.SO4)
        self.pressionSensor = BMP085.BMP085(busnum=1, mode=BMP085.BMP085_ULTRAHIGHRES)
        self.gasSensor = BMP085.BMP085(busnum=4, mode=BMP085.BMP085_ULTRAHIGHRES)
        
        self.__avgPression = 0
        self.__avgGas = 0
        
        self.__reCalibrate = False
        
        self.stop = False

    def kill(self):
        self.stop = True
    
    def setReCalibrate(self, state):
        if state is not None:
            self.__reCalibrate = state

    def calibratePressionSensors(self):
        self.controller.notify(MSG["calibration"])
        sum = self.aggregateReads(self.pressionSensor, 3)
        self.__avgPression = sum // 3

        sum = self.aggregateReads(self.gasSensor, 3)
        self.__avgGas = sum // 3
    
    def aggregateReads(self, sensor, num):
        sum = 0
        for i in range(num):
            sum += sensor.read_pressure()
            time.sleep(0.03)
            
        return sum
        
    def run(self):
        """ calibrate sensors"""
        self.calibratePressionSensors()

        self.controller.notify(MSG["startup"])
        
        while not self.stop:
            
            if self.__reCalibrate:
                self.calibratePressionSensors()
                self.__reCalibrate = False
                
            """ get data """
            ovenTemp = self.ovenThermocouple.readTempC()
            floorTemp = self.floorThermocouple.readTempC()
            pufferTemp = self.pufferThermocouple.readTempC()
            fumesTemp = self.fumesThermocouple.readTempC()
            """
            pression1 = self.pressionSensor.read_pressure()
            delta1 = pression1 - mean1
            
            pression2 = self.gasSensor.read_pressure()
            delta2 = pression2 - mean2
            """
#             pression1 = self.aggregateReads(self.pressionSensor, 10) // 10
            pression1 = self.pressionSensor.read_pressure()
            delta1 = pression1 - self.__avgPression
            
#             pression2 = self.aggregateReads(self.gasSensor, 10) // 10
            pression2 = self.gasSensor.read_pressure()
            delta2 = pression2 - self.__avgGas
            
            """ display data """
            self.controller.setData(ovenTemp, floorTemp, pufferTemp, fumesTemp, delta1, delta2)

            """ persist data """
            if self.controller.config["persistData"]:
                
                """ Build query string """
                insert_string = "INSERT INTO Temperatures VALUES(datetime('now', 'localtime')"
                        
                if not isnan(ovenTemp):
                    insert_string += ", " + str(ovenTemp)
                else:
                    insert_string += ", NULL"
                    
                if not isnan(floorTemp):
                    insert_string += ", " + str(floorTemp)
                else:
                    insert_string += ", NULL"
                    
                if not isnan(pufferTemp):
                    insert_string += ", " + str(pufferTemp)
                else:
                    insert_string += ", NULL"
                    
                if not isnan(fumesTemp):
                    insert_string += ", " + str(fumesTemp)
                else:
                    insert_string += ", NULL"
                    
                insert_string += ")"
                        
                try:
                    con = sqlite3.connect('oven.db')
                    with con:
                        cur = con.cursor()                        
                        cur.execute(insert_string)
                        con.commit() 
                except:
                    print("Couldn't write on DB")
                    self.controller.notifyCritical(MSG["DB_error"])
                    
            time.sleep(SLEEP_TIME)
