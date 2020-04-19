#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
from math import isnan
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import *
from utils.messages import CHARTS_CONTROLLER_MSGS as MSG

AXISX_RANGE = 180 #(seconds)
BASE_Y_MAX_VALUE = 40 #(degree Celsius)
"""
class Chart(QChart):
    
    def __init__(self):
        super().__init__()
        self.grabGesture(QtCore.Qt.PanGesture)
        self.grabGesture(QtCore.Qt.PinchGesture)
        
    def sceneEvent(self, event):
        if event.type() == QtCore.QEvent.Gesture:
            print("Gesture")
            
        if event.type() == QtCore.Qt.PanGesture:
            print("Pan")
            
        if event.type() == QtCore.Qt.PinchGesture:
            print("Pinch")
        print(event.type())
            
        return super().event(event)
"""     

class ChartsController(object):
    def __init__(self, container):
        """ Layout to fill with chart """
        self.container = container
        """ Max Y axis value """
        self.upperYValue = BASE_Y_MAX_VALUE
        
        self.setupCharts()
        
    def setupCharts(self):
        
        """ Main chart object """
        self.chart = QChart()
        self.chart.legend().setVisible(True)
        self.chart.setTitle("Andamento temperatura.")
        #self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTheme(QChart.ChartThemeBrownSand)
        
        
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
        self.chart.addAxis(self.axisX, QtCore.Qt.AlignBottom)   
        
        self.axisY = QValueAxis()
        self.axisY.setLabelFormat("%i")
        self.axisY.setTitleText("Temperatura")
        self.axisY.setRange(0, self.upperYValue)
        self.chart.addAxis(self.axisY, QtCore.Qt.AlignLeft)
        
        self.updateAxis()
        
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
        #self.chartView.setRubberBand(QChartView.HorizontalRubberBand)
        
        self.container.addWidget(self.chartView, 1, 1)
        
        
    def getData(self, interval):
        """ Retrieve data from db """
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
        except:
            print("Couldn't read from DB")
            #self.controller.notifyCritical(MSG["DB_error"])
            
        return records
    
    def toggleOvenSerie(self, state):
        """ Display/Hide oven temperatures """
        if state:
            self.ovenSerie.show()
        else:
            self.ovenSerie.hide()
            
    def toggleFloorSerie(self, state):
        """ Display/Hide floor temperatures """
        if state:
            self.floorSerie.show()
        else:
            self.floorSerie.hide()
            
    def togglePufferSerie(self, state):
        """ Display/Hide puffer temperatures """
        if state:
            self.pufferSerie.show()
        else:
            self.pufferSerie.hide()
            
    def toggleFumesSerie(self, state):
        """ Display/Hide fumes temperatures """
        if state:
            self.fumesSerie.show()
        else:
            self.fumesSerie.hide()
             
    def toggleRealTimeTracking(self, state):
        """ Updates axis X range / clear chart """
        if state:
            self.updateAxis()
        else:
            self.clearSeries()
        
    def updateAxis(self):
        """ Set time range """
        currentTime =  QtCore.QDateTime.currentDateTime()
        self.axisX.setRange(currentTime, currentTime.addSecs(AXISX_RANGE))
        self.upperYValue = BASE_Y_MAX_VALUE
        self.axisY.setRange(0, self.upperYValue)
        
    def updateChartRealTime(self, ovenTemp, floorTemp, pufferTemp, fumesTemp):
        """ Updates chart with real time data from sensors """
        currentTime =  QtCore.QDateTime.currentDateTime()
        if self.axisX.max() <= currentTime:
            self.updateAxis()
            self.clearSeries()
            
            
        self.axisX.setFormat("hh:mm:ss")
        self.axisX.setTickCount(10)
        self.updateUpperYValue([ovenTemp, floorTemp, pufferTemp, fumesTemp])
        
        currentTimeMsec = currentTime.toMSecsSinceEpoch()
        self.appendData(currentTimeMsec, ovenTemp, floorTemp, pufferTemp, fumesTemp)
        
    def appendData(self, datetime, ovenTemp, floorTemp, pufferTemp, fumesTemp):
        """ Append data to series """
        if not isnan(ovenTemp):
            self.ovenSerie.append(datetime, ovenTemp)
        if not isnan(floorTemp):
            self.floorSerie.append(datetime, floorTemp)
        if not isnan(pufferTemp):
            self.pufferSerie.append(datetime, pufferTemp)
        if not isnan(fumesTemp):
            self.fumesSerie.append(datetime, fumesTemp)
        
    def updateUpperYValue(self, temps = None):
        """ Update upper axis Y value based on max series value """
        MAX = 0
        
        if temps is not None:
            """ real time """
            list = []
            """ filter nan """
            for temp in temps:
                if not isnan(temp):
                    list.append(temp)
                    
            MAX = max(list)
        else:
            """ interval drawing """
            MAX = max(self.max(self.ovenSerie),
                      self.max(self.floorSerie),
                      self.max(self.pufferSerie),
                      self.max(self.fumesSerie))
            
        if MAX > self.upperYValue:
            self.upperYValue = MAX + 10
            self.axisY.setRange(0, self.upperYValue)
             
    def max(self, serie):
        max = 0
        for val in serie.pointsVector():
            if val.y() > max:
                max = val.y()
        return max
    
    def clearSeries(self):
        self.ovenSerie.clear()
        self.floorSerie.clear()
        self.pufferSerie.clear()
        self.fumesSerie.clear()
        
    def draw(self, interval):
        """ Main function to draw chart based on interval """
        self.clearSeries()
        self.upperYValue = BASE_Y_MAX_VALUE
        self.axisY.setRange(0, self.upperYValue)
        data = self.getData(interval) # Python list
        data = self.resampleData(data, interval) # pandas DataFrame (resampled data)
        self.updateAxisXInterval(data['Timestamp'].iloc[0], data['Timestamp'].iloc[-1], interval)     
        self.buildSeries(data)
        self.updateUpperYValue()
    
    def resampleData(self, data, interval):
        """ Converts data to pandas DataFrame type and perform resampling """
        df = pd.DataFrame(data, columns=['Timestamp', 'OvenTemp', 'FloorTemp', 'PufferTemp', 'FumesTemp'])
        df = df.assign(Timestamp=pd.to_datetime(df.Timestamp))
        
        if interval == "hour":
            df = df.resample('1min', on='Timestamp')
        elif interval == "day":
            df = df.resample('5min', on='Timestamp')
        elif interval == "week":
            df = df.resample('20min', on='Timestamp')
            
        df = df.mean().reset_index().interpolate()
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
        if(data.shape[1] > 4):
            for index, row in data.iterrows():
                datetimeString = row[0].strftime("%Y/%m/%d %H:%M:%S")
                datetime = QtCore.QDateTime.fromString(datetimeString, "yyyy/MM/dd HH:mm:ss").toMSecsSinceEpoch()    
                self.appendData(datetime, row[1], row[2], row[3], row[4])
        else:
            self.controller.notifyCritical(MSG["chart_drawing_error"])
            
