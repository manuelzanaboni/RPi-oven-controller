#!/usr/bin/python3
# coding: utf8

import sqlite3
import sys
import time
import random
from threading import Thread

# import RPi.GPIO as GPIO
import default_gpio as PIN
import MAX6675.MAX6675 as MAX6675
import Adafruit_BMP.BMP085 as BMP085

class SensReader(Thread):
    def __init__(self, controller):
        super(SensReader, self).__init__()
        self.controller = controller

        # ovenThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS1, PIN.SO1)
        # floorThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS2, PIN.SO2)
        # pufferThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS3, PIN.SO3)
        # fumesThermocouple = MAX6675.MAX6675(PIN.CLK, PIN.CS4, PIN.SO4)

    def run(self):
        while True:
            # ovenTemp = ovenThermocouple.readTempC()
            # floorTemp = floorThermocouple.readTempC()
            # pufferTemp = pufferThermocouple.readTempC()
            # fumesTemp = fumesThermocouple.readTempC()

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

            # self.controller.setData(ovenTemp, floorTemp, pufferTemp, fumesTemp)
            time.sleep(3)
