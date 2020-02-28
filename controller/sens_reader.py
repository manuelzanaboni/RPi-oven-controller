#!/usr/bin/python3
# coding: utf8

import sqlite3
import sys
import time
import random
from threading import Thread

import default_gpio as PIN
import MAX6675.MAX6675 as MAX6675
import Adafruit_BMP.BMP085 as BMP085

class SensReader(Thread):
    def __init__(self, controller):
        super(SensReader, self).__init__()
        self.controller = controller

        self.ovenThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS1, PIN.SO1)
        self.floorThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS2, PIN.SO2)
        self.pufferThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS3, PIN.SO3)
        self.fumesThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS4, PIN.SO4)
        self.pressionSensor = BMP085.BMP085()
        
        self.stop = False

    def kill(self):
        self.stop = True
        
    def run(self):
        sum = 0
        #self.controller.notify("Avviamento procedura di calibrazione pressione")
        for i in range(10):
            sum += self.pressionSensor.read_pressure()
            time.sleep(0.3)
        
        mean = sum // 10

        while not self.stop:
            ovenTemp = self.ovenThermocouple.readTempC()
            floorTemp = self.floorThermocouple.readTempC()
            pufferTemp = self.pufferThermocouple.readTempC()
            fumesTemp = self.fumesThermocouple.readTempC()
            pression = self.pressionSensor.read_pressure()
            
            delta = pression - mean

            # DB signature
            # TABLE OvenTemperatures(timestamp DATETIME, temp NUMERIC)
            # TABLE FloorTemperatures(timestamp DATETIME, temp NUMERIC)
            # TABLE PufferTemperatures(timestamp DATETIME, temp NUMERIC)
            # TABLE FumesTemperatures(timestamp DATETIME, temp NUMERIC)
            # TABLE OvenPression(timestamp DATETIME, pression NUMERIC)


            # con = sqlite3.connect('primoDB.db')
            # with con:
            #     cur = con.cursor()
                
                # cur.execute("INSERT INTO OvenTemperatures VALUES(datetime('now','+1 hour'), " + str(x) + ")")
                # cur.execute("INSERT INTO FloorTemperatures VALUES(datetime('now','+1 hour'), " + str(x) + ")")
                # cur.execute("INSERT INTO PufferTemperatures VALUES(datetime('now','+1 hour'), " + str(x) + ")")
                # cur.execute("INSERT INTO FumesTemperatures VALUES(datetime('now','+1 hour'), " + str(x) + ")")
            #     con.commit()
            # con.close()

            self.controller.setData(ovenTemp, floorTemp, pufferTemp, fumesTemp, delta)
            time.sleep(3)
