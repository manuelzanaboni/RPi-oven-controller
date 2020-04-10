#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import *

import pandas as pd
import sqlite3
import time

class ChartsController(object):
    def __init__(self, container):
        """ Layout to fill with chart """
        self.container = container
        """ Max Y axis value """
        self.upperYValue = 40
        
        self.setupCharts()
        
    def setupCharts(self):
        
        """ Main chart object """
        self.chart = QChart()
        self.chart.legend().setVisible(True)
        self.chart.setTitle("Andamento temperatura.")
        #self.chart.setAnimationOptions(QChart.SeriesAnimations)
        
        """ Series definition """
        self.ovenSerie = QLineSeries()
        self.ovenSerie.setName("Forno")
        
        self.floorSerie = QLineSeries()
        self.floorSerie.setName("Platea")
        
        self.pufferSerie = QLineSeries()
        self.pufferSerie.setName("Puffer")
        
        self.fumesSerie = QLineSeries()
        self.fumesSerie.setName("Fumi")
        
        self.chart.addSeries(self.ovenSerie)
        self.chart.addSeries(self.floorSerie)
        self.chart.addSeries(self.pufferSerie)
        self.chart.addSeries(self.fumesSerie)
            
        """ Axis definitions """
        self.axisX = QDateTimeAxis()
        self.axisX.setFormat("hh:mm:ss")
        self.axisX.setTickCount(10)
        self.axisX.setTitleText("Tempo")
        self.updateAxisX()
        self.chart.addAxis(self.axisX, QtCore.Qt.AlignBottom)   
        
        self.axisY = QValueAxis()
        self.axisY.setLabelFormat("%i")
        self.axisY.setTitleText("Temperatura")
        self.axisY.setRange(0, self.upperYValue)
        self.chart.addAxis(self.axisY, QtCore.Qt.AlignLeft)
        
        self.ovenSerie.attachAxis(self.axisX)
        self.ovenSerie.attachAxis(self.axisY)
        self.floorSerie.attachAxis(self.axisX)
        self.floorSerie.attachAxis(self.axisY)
        self.pufferSerie.attachAxis(self.axisX)
        self.pufferSerie.attachAxis(self.axisY)
        self.fumesSerie.attachAxis(self.axisX)
        self.fumesSerie.attachAxis(self.axisY)

        """ Chart View """
        self.chartView = QChartView(self.chart)
        self.chartView.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.container.addWidget(self.chartView, 1, 1)
        
    def toggleOvenSerie(self, state):
        if state:
            self.ovenSerie.show()
        else:
            self.ovenSerie.hide()
            
    def toggleFloorSerie(self, state):
        if state:
            self.floorSerie.show()
        else:
            self.floorSerie.hide()
            
    def togglePufferSerie(self, state):
        if state:
            self.pufferSerie.show()
        else:
            self.pufferSerie.hide()
            
    def toggleFumesSerie(self, state):
        if state:
            self.fumesSerie.show()
        else:
            self.fumesSerie.hide()
             
    def toggleRealTimeTracking(self, state):
        if state:
            self.updateAxisX()
        else:
            self.clearSeries()
        
    def updateAxisX(self):
        currentTime =  QtCore.QDateTime.currentDateTime()
        self.axisX.setRange(currentTime, currentTime.addSecs(120))
        
    def updateChartRealTime(self, ovenTemp, floorTemp, pufferTemp, fumesTemp):
        currentTime =  QtCore.QDateTime.currentDateTime()
        if self.axisX.max() <= currentTime:
            self.updateAxisX()
            self.clearSeries()
            
        self.axisX.setFormat("hh:mm:ss")
        self.axisX.setTickCount(10)
        self.updateUpperYValue()
        
        self.ovenSerie.append(currentTime.toMSecsSinceEpoch(), ovenTemp)
        self.floorSerie.append(currentTime.toMSecsSinceEpoch(), floorTemp)
        self.pufferSerie.append(currentTime.toMSecsSinceEpoch(), pufferTemp)
        self.fumesSerie.append(currentTime.toMSecsSinceEpoch(), fumesTemp)
        
    def updateUpperYValue(self):
        max = 0
        
        for val in self.ovenSerie.pointsVector():
            if val.y() > max:
                max = val.y()
                
        for val in self.floorSerie.pointsVector():
            if val.y() > max:
                max = val.y()
                
        for val in self.pufferSerie.pointsVector():
            if val.y() > max:
                max = val.y()
                
        for val in self.fumesSerie.pointsVector():
            if val.y() > max:
                max = val.y()
                
        if max > self.upperYValue:
            self.upperYValue = max + 10
            self.axisY.setRange(0, self.upperYValue)
                
    def clearSeries(self):
        self.ovenSerie.clear()
        self.floorSerie.clear()
        self.pufferSerie.clear()
        self.fumesSerie.clear()
        
    def draw(self, interval):
        self.clearSeries()
        data = self.getData(interval) # Python list
        print(len(data))
        data = self.resampleData(data, interval) # pandas DataFrame
        print(data)
        self.updateAxisXInterval(data['Timestamp'].iloc[0], data['Timestamp'].iloc[-1], interval)     
        self.buildSeries(data)
        """
        self.updateUpperYValue()
        """
    
    def getData(self, interval):
        query_string = ""
        
        if interval == "hour":
            query_string = "SELECT * FROM Temperatures WHERE Timestamp > DATETIME('now', 'localtime', '-1 hour');"
        elif interval == "day":
            query_string = "SELECT * FROM Temperatures WHERE Timestamp > DATETIME('now', 'localtime', '-1 day');"
        elif interval == "week":
            query_string = "SELECT * FROM Temperatures WHERE Timestamp > DATETIME('now', 'localtime', '-7 days');"
        
        records = []
        
        try:
            con = sqlite3.connect('oven.db')
            with con:
                cur = con.cursor()                        
                cur.execute(query_string)
                records = cur.fetchall()
                cur.close()
            con.close()
        except:
            print("Couldn't read from DB")
            #self.controller.notifyCritical(MSG["DB_error"])
            
        return records
    
    def resampleData(self, data, interval):
        df = pd.DataFrame(data, columns=['Timestamp', 'OvenTemp', 'FloorTemp', 'PufferTemp', 'FumesTemp'])
        df = df.assign(Timestamp=pd.to_datetime(df.Timestamp))
        
        if interval == "hour":
            df = df.resample('1min', on='Timestamp').mean().reset_index().interpolate()
        elif interval == "day":
            df = df.resample('5min', on='Timestamp').mean().reset_index().interpolate()
        elif interval == "week":
            df = df.resample('20min', on='Timestamp').mean().reset_index().interpolate()
        
        return df
            
    def updateAxisXInterval(self, min, max, interval):        
        if interval == "week":
            self.axisX.setFormat("dd/MM/yyyy")
            self.axisX.setTickCount(7)
        elif interval == "day":
            self.axisX.setFormat("hh:mm")
            self.axisX.setTickCount(10)
        else:
            self.axisX.setFormat("hh:mm:ss")
            self.axisX.setTickCount(10)
        self.axisX.setRange(min, max)
        
    def buildSeries(self, data):
        for index, row in data.iterrows():
            #datetime = QtCore.QDateTime.fromString(tuple[0], "yyyy-MM-dd HH:mm:ss").toMSecsSinceEpoch()
            #datetime = time.mktime(pd.Timestamp(row[0]).timetuple())
            datetime = time.mktime(row[0].timetuple())
            self.ovenSerie.append(datetime, row[1])
            self.floorSerie.append(datetime, row[2])
            self.pufferSerie.append(datetime, row[3])
            self.fumesSerie.append(datetime, row[4])

            
            