#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import ui.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 501, 91))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        self.temperatureOvenLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.temperatureOvenLabel.setFont(font)
        self.temperatureOvenLabel.setWordWrap(False)
        self.temperatureOvenLabel.setObjectName("temperatureOvenLabel")
        self.horizontalLayout1.addWidget(self.temperatureOvenLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout1.addItem(spacerItem)
        self.ovenLCD = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ovenLCD.sizePolicy().hasHeightForWidth())
        self.ovenLCD.setSizePolicy(sizePolicy)
        self.ovenLCD.setMinimumSize(QtCore.QSize(85, 85))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.ovenLCD.setFont(font)
        self.ovenLCD.setFrameShape(QtWidgets.QFrame.Box)
        self.ovenLCD.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ovenLCD.setDigitCount(3)
        self.ovenLCD.setObjectName("ovenLCD")
        self.horizontalLayout1.addWidget(self.ovenLCD)
        self.degreeLabel1 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        self.degreeLabel1.setFont(font)
        self.degreeLabel1.setWordWrap(False)
        self.degreeLabel1.setObjectName("degreeLabel1")
        self.horizontalLayout1.addWidget(self.degreeLabel1)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 110, 501, 91))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.temperatureFloorLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.temperatureFloorLabel.setFont(font)
        self.temperatureFloorLabel.setWordWrap(False)
        self.temperatureFloorLabel.setObjectName("temperatureFloorLabel")
        self.horizontalLayout2.addWidget(self.temperatureFloorLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem1)
        self.floorLCD = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.floorLCD.sizePolicy().hasHeightForWidth())
        self.floorLCD.setSizePolicy(sizePolicy)
        self.floorLCD.setMinimumSize(QtCore.QSize(85, 85))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.floorLCD.setFont(font)
        self.floorLCD.setFrameShape(QtWidgets.QFrame.Box)
        self.floorLCD.setFrameShadow(QtWidgets.QFrame.Raised)
        self.floorLCD.setDigitCount(3)
        self.floorLCD.setObjectName("floorLCD")
        self.horizontalLayout2.addWidget(self.floorLCD)
        self.degreeLabel2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        self.degreeLabel2.setFont(font)
        self.degreeLabel2.setWordWrap(False)
        self.degreeLabel2.setObjectName("degreeLabel2")
        self.horizontalLayout2.addWidget(self.degreeLabel2)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 200, 501, 91))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout3.setObjectName("horizontalLayout3")
        self.temperaturePufferLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.temperaturePufferLabel.setFont(font)
        self.temperaturePufferLabel.setWordWrap(False)
        self.temperaturePufferLabel.setObjectName("temperaturePufferLabel")
        self.horizontalLayout3.addWidget(self.temperaturePufferLabel)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout3.addItem(spacerItem2)
        self.pufferLCD = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pufferLCD.sizePolicy().hasHeightForWidth())
        self.pufferLCD.setSizePolicy(sizePolicy)
        self.pufferLCD.setMinimumSize(QtCore.QSize(85, 85))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.pufferLCD.setFont(font)
        self.pufferLCD.setFrameShape(QtWidgets.QFrame.Box)
        self.pufferLCD.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pufferLCD.setDigitCount(3)
        self.pufferLCD.setObjectName("pufferLCD")
        self.horizontalLayout3.addWidget(self.pufferLCD)
        self.degreeLabel3 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        self.degreeLabel3.setFont(font)
        self.degreeLabel3.setWordWrap(False)
        self.degreeLabel3.setObjectName("degreeLabel3")
        self.horizontalLayout3.addWidget(self.degreeLabel3)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 290, 501, 91))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout4.setObjectName("horizontalLayout4")
        self.temperatureFumesLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.temperatureFumesLabel.setFont(font)
        self.temperatureFumesLabel.setWordWrap(False)
        self.temperatureFumesLabel.setObjectName("temperatureFumesLabel")
        self.horizontalLayout4.addWidget(self.temperatureFumesLabel)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout4.addItem(spacerItem3)
        self.fumesLCD = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fumesLCD.sizePolicy().hasHeightForWidth())
        self.fumesLCD.setSizePolicy(sizePolicy)
        self.fumesLCD.setMinimumSize(QtCore.QSize(85, 85))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.fumesLCD.setFont(font)
        self.fumesLCD.setFrameShape(QtWidgets.QFrame.Box)
        self.fumesLCD.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fumesLCD.setDigitCount(3)
        self.fumesLCD.setObjectName("fumesLCD")
        self.horizontalLayout4.addWidget(self.fumesLCD)
        self.degreeLabel4 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        self.degreeLabel4.setFont(font)
        self.degreeLabel4.setWordWrap(False)
        self.degreeLabel4.setObjectName("degreeLabel4")
        self.horizontalLayout4.addWidget(self.degreeLabel4)
        self.thermostatLabel = QtWidgets.QLabel(self.centralwidget)
        self.thermostatLabel.setGeometry(QtCore.QRect(10, 410, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.thermostatLabel.setFont(font)
        self.thermostatLabel.setWordWrap(False)
        self.thermostatLabel.setObjectName("thermostatLabel")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(10, 450, 501, 91))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout5.setObjectName("horizontalLayout5")
        self.decrementThermostatButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        self.decrementThermostatButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/src/thermostatDown.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.decrementThermostatButton.setIcon(icon)
        self.decrementThermostatButton.setIconSize(QtCore.QSize(64, 64))
        self.decrementThermostatButton.setAutoRepeat(True)
        self.decrementThermostatButton.setAutoRepeatDelay(100)
        self.decrementThermostatButton.setAutoRepeatInterval(400)
        self.decrementThermostatButton.setAutoDefault(False)
        self.decrementThermostatButton.setDefault(False)
        self.decrementThermostatButton.setFlat(True)
        self.decrementThermostatButton.setObjectName("decrementThermostatButton")
        self.horizontalLayout5.addWidget(self.decrementThermostatButton)
        self.horizontalSlider = QtWidgets.QSlider(self.horizontalLayoutWidget_5)
        self.horizontalSlider.setMinimum(100)
        self.horizontalSlider.setMaximum(550)
        self.horizontalSlider.setSingleStep(5)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(50)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout5.addWidget(self.horizontalSlider)
        self.incrementThermostatButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        self.incrementThermostatButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/src/thermostatUp.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.incrementThermostatButton.setIcon(icon1)
        self.incrementThermostatButton.setIconSize(QtCore.QSize(64, 64))
        self.incrementThermostatButton.setAutoRepeat(True)
        self.incrementThermostatButton.setAutoRepeatDelay(100)
        self.incrementThermostatButton.setAutoRepeatInterval(400)
        self.incrementThermostatButton.setAutoDefault(False)
        self.incrementThermostatButton.setDefault(False)
        self.incrementThermostatButton.setFlat(True)
        self.incrementThermostatButton.setObjectName("incrementThermostatButton")
        self.horizontalLayout5.addWidget(self.incrementThermostatButton)
        self.thermostatLCD = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thermostatLCD.sizePolicy().hasHeightForWidth())
        self.thermostatLCD.setSizePolicy(sizePolicy)
        self.thermostatLCD.setMinimumSize(QtCore.QSize(100, 0))
        self.thermostatLCD.setMaximumSize(QtCore.QSize(16777215, 60))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 1, 5))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 1, 5))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(157, 157, 157))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.thermostatLCD.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.thermostatLCD.setFont(font)
        self.thermostatLCD.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.thermostatLCD.setFrameShadow(QtWidgets.QFrame.Raised)
        self.thermostatLCD.setDigitCount(3)
        self.thermostatLCD.setProperty("value", 100.0)
        self.thermostatLCD.setObjectName("thermostatLCD")
        self.horizontalLayout5.addWidget(self.thermostatLCD)
        self.thermostatDegreeLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(34)
        font.setBold(False)
        font.setWeight(50)
        self.thermostatDegreeLabel.setFont(font)
        self.thermostatDegreeLabel.setWordWrap(False)
        self.thermostatDegreeLabel.setObjectName("thermostatDegreeLabel")
        self.horizontalLayout5.addWidget(self.thermostatDegreeLabel)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(17, 390, 491, 20))
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lightButton = QtWidgets.QPushButton(self.centralwidget)
        self.lightButton.setGeometry(QtCore.QRect(540, 190, 88, 76))
        self.lightButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/src/lightOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/src/lightOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.lightButton.setIcon(icon2)
        self.lightButton.setIconSize(QtCore.QSize(64, 64))
        self.lightButton.setCheckable(True)
        self.lightButton.setAutoDefault(False)
        self.lightButton.setDefault(False)
        self.lightButton.setFlat(True)
        self.lightButton.setObjectName("lightButton")
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(541, 20, 421, 91))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.horizontalLayout6 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout6.setObjectName("horizontalLayout6")
        self.pressionLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.pressionLabel.setFont(font)
        self.pressionLabel.setWordWrap(False)
        self.pressionLabel.setObjectName("pressionLabel")
        self.horizontalLayout6.addWidget(self.pressionLabel)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout6.addItem(spacerItem4)
        self.pressureLCD = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pressureLCD.sizePolicy().hasHeightForWidth())
        self.pressureLCD.setSizePolicy(sizePolicy)
        self.pressureLCD.setMinimumSize(QtCore.QSize(85, 85))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.pressureLCD.setFont(font)
        self.pressureLCD.setFrameShape(QtWidgets.QFrame.Box)
        self.pressureLCD.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pressureLCD.setDigitCount(3)
        self.pressureLCD.setObjectName("pressureLCD")
        self.horizontalLayout6.addWidget(self.pressureLCD)
        self.pressureLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        self.pressureLabel.setFont(font)
        self.pressureLabel.setWordWrap(False)
        self.pressureLabel.setObjectName("pressureLabel")
        self.horizontalLayout6.addWidget(self.pressureLabel)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(520, 20, 16, 361))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.line_2.setFont(font)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setLineWidth(1)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.timerFrame = QtWidgets.QFrame(self.centralwidget)
        self.timerFrame.setGeometry(QtCore.QRect(680, 390, 331, 151))
        self.timerFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.timerFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.timerFrame.setObjectName("timerFrame")
        self.horizontalLayoutWidget_7 = QtWidgets.QWidget(self.timerFrame)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(0, 0, 331, 152))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")
        self.horizontalLayout7 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout7.setObjectName("horizontalLayout7")
        self.timerLCD = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timerLCD.sizePolicy().hasHeightForWidth())
        self.timerLCD.setSizePolicy(sizePolicy)
        self.timerLCD.setMinimumSize(QtCore.QSize(85, 85))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.timerLCD.setFont(font)
        self.timerLCD.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.timerLCD.setFrameShadow(QtWidgets.QFrame.Plain)
        self.timerLCD.setDigitCount(5)
        self.timerLCD.setProperty("value", 0.0)
        self.timerLCD.setObjectName("timerLCD")
        self.horizontalLayout7.addWidget(self.timerLCD)
        self.horizontalLayout8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout8.setObjectName("horizontalLayout8")
        self.verticalLayout1 = QtWidgets.QVBoxLayout()
        self.verticalLayout1.setObjectName("verticalLayout1")
        self.increaseTimerButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_7)
        self.increaseTimerButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/src/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.increaseTimerButton.setIcon(icon3)
        self.increaseTimerButton.setIconSize(QtCore.QSize(56, 56))
        self.increaseTimerButton.setAutoDefault(False)
        self.increaseTimerButton.setDefault(False)
        self.increaseTimerButton.setFlat(True)
        self.increaseTimerButton.setObjectName("increaseTimerButton")
        self.verticalLayout1.addWidget(self.increaseTimerButton)
        self.decreaseTimerButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_7)
        self.decreaseTimerButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/src/minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.decreaseTimerButton.setIcon(icon4)
        self.decreaseTimerButton.setIconSize(QtCore.QSize(56, 56))
        self.decreaseTimerButton.setAutoDefault(False)
        self.decreaseTimerButton.setDefault(False)
        self.decreaseTimerButton.setFlat(True)
        self.decreaseTimerButton.setObjectName("decreaseTimerButton")
        self.verticalLayout1.addWidget(self.decreaseTimerButton)
        self.horizontalLayout8.addLayout(self.verticalLayout1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.startTimerButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_7)
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.startTimerButton.setFont(font)
        self.startTimerButton.setFlat(True)
        self.startTimerButton.setObjectName("startTimerButton")
        self.verticalLayout.addWidget(self.startTimerButton)
        self.stopTimerButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_7)
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.stopTimerButton.setFont(font)
        self.stopTimerButton.setAutoDefault(False)
        self.stopTimerButton.setFlat(True)
        self.stopTimerButton.setObjectName("stopTimerButton")
        self.verticalLayout.addWidget(self.stopTimerButton)
        self.resetTimerButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_7)
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.resetTimerButton.setFont(font)
        self.resetTimerButton.setFlat(True)
        self.resetTimerButton.setObjectName("resetTimerButton")
        self.verticalLayout.addWidget(self.resetTimerButton)
        self.horizontalLayout8.addLayout(self.verticalLayout)
        self.horizontalLayout7.addLayout(self.horizontalLayout8)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(850, 150, 78, 111))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout3.setSpacing(0)
        self.verticalLayout3.setObjectName("verticalLayout3")
        self.intLabel = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.intLabel.setFont(font)
        self.intLabel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.intLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.intLabel.setObjectName("intLabel")
        self.verticalLayout3.addWidget(self.intLabel)
        self.internalOpeningButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.internalOpeningButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/src/openingOpen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap(":/src/openingClose.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.internalOpeningButton.setIcon(icon5)
        self.internalOpeningButton.setIconSize(QtCore.QSize(64, 64))
        self.internalOpeningButton.setCheckable(True)
        self.internalOpeningButton.setAutoDefault(False)
        self.internalOpeningButton.setDefault(False)
        self.internalOpeningButton.setFlat(True)
        self.internalOpeningButton.setObjectName("internalOpeningButton")
        self.verticalLayout3.addWidget(self.internalOpeningButton)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(930, 150, 78, 111))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout4.setSpacing(0)
        self.verticalLayout4.setObjectName("verticalLayout4")
        self.estLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.estLabel.setFont(font)
        self.estLabel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.estLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.estLabel.setObjectName("estLabel")
        self.verticalLayout4.addWidget(self.estLabel)
        self.externalOpeningButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.externalOpeningButton.setText("")
        self.externalOpeningButton.setIcon(icon5)
        self.externalOpeningButton.setIconSize(QtCore.QSize(64, 64))
        self.externalOpeningButton.setCheckable(True)
        self.externalOpeningButton.setAutoDefault(False)
        self.externalOpeningButton.setDefault(False)
        self.externalOpeningButton.setFlat(True)
        self.externalOpeningButton.setObjectName("externalOpeningButton")
        self.verticalLayout4.addWidget(self.externalOpeningButton)
        self.steamButton = QtWidgets.QPushButton(self.centralwidget)
        self.steamButton.setGeometry(QtCore.QRect(640, 190, 88, 76))
        self.steamButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/src/steam.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.steamButton.setIcon(icon6)
        self.steamButton.setIconSize(QtCore.QSize(76, 76))
        self.steamButton.setCheckable(False)
        self.steamButton.setAutoDefault(False)
        self.steamButton.setDefault(False)
        self.steamButton.setFlat(True)
        self.steamButton.setObjectName("steamButton")
        self.fanButton = QtWidgets.QPushButton(self.centralwidget)
        self.fanButton.setGeometry(QtCore.QRect(740, 190, 88, 76))
        self.fanButton.setText("")
        self.fanButton.setIconSize(QtCore.QSize(76, 76))
        self.fanButton.setCheckable(False)
        self.fanButton.setAutoDefault(False)
        self.fanButton.setDefault(False)
        self.fanButton.setFlat(True)
        self.fanButton.setObjectName("fanButton")
        self.alexaButton = QtWidgets.QPushButton(self.centralwidget)
        self.alexaButton.setGeometry(QtCore.QRect(920, 290, 88, 76))
        self.alexaButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/src/alexaOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon7.addPixmap(QtGui.QPixmap(":/src/alexaOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.alexaButton.setIcon(icon7)
        self.alexaButton.setIconSize(QtCore.QSize(64, 64))
        self.alexaButton.setCheckable(True)
        self.alexaButton.setAutoDefault(False)
        self.alexaButton.setDefault(False)
        self.alexaButton.setFlat(True)
        self.alexaButton.setObjectName("alexaButton")
        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        self.quitButton.setGeometry(QtCore.QRect(970, 10, 51, 51))
        self.quitButton.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/src/quit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quitButton.setIcon(icon8)
        self.quitButton.setIconSize(QtCore.QSize(50, 50))
        self.quitButton.setCheckable(False)
        self.quitButton.setAutoDefault(False)
        self.quitButton.setDefault(False)
        self.quitButton.setFlat(True)
        self.quitButton.setObjectName("quitButton")
        self.burnerButton = QtWidgets.QPushButton(self.centralwidget)
        self.burnerButton.setGeometry(QtCore.QRect(570, 460, 76, 70))
        self.burnerButton.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/src/OnOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.burnerButton.setIcon(icon9)
        self.burnerButton.setIconSize(QtCore.QSize(64, 64))
        self.burnerButton.setAutoDefault(False)
        self.burnerButton.setDefault(False)
        self.burnerButton.setFlat(True)
        self.burnerButton.setObjectName("burnerButton")
        self.burnerLabel = QtWidgets.QLabel(self.centralwidget)
        self.burnerLabel.setGeometry(QtCore.QRect(570, 380, 54, 17))
        self.burnerLabel.setText("")
        self.burnerLabel.setObjectName("burnerLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.horizontalSlider.valueChanged['int'].connect(self.thermostatLCD.display)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Gestione Forno"))
        self.temperatureOvenLabel.setText(_translate("MainWindow", "Temperatura forno"))
        self.degreeLabel1.setText(_translate("MainWindow", "°C"))
        self.temperatureFloorLabel.setText(_translate("MainWindow", "Temperatura platea"))
        self.degreeLabel2.setText(_translate("MainWindow", "°C"))
        self.temperaturePufferLabel.setText(_translate("MainWindow", "Temperatura puffer"))
        self.degreeLabel3.setText(_translate("MainWindow", "°C"))
        self.temperatureFumesLabel.setText(_translate("MainWindow", "Temperatura u. fumi"))
        self.degreeLabel4.setText(_translate("MainWindow", "°C"))
        self.thermostatLabel.setText(_translate("MainWindow", "Imposta temperatura"))
        self.thermostatDegreeLabel.setText(_translate("MainWindow", "°C"))
        self.pressionLabel.setText(_translate("MainWindow", "Pressione forno"))
        self.pressureLabel.setText(_translate("MainWindow", "Pa"))
        self.startTimerButton.setText(_translate("MainWindow", "Avvia"))
        self.stopTimerButton.setText(_translate("MainWindow", "Ferma"))
        self.resetTimerButton.setText(_translate("MainWindow", "Reset"))
        self.intLabel.setText(_translate("MainWindow", "INT"))
        self.estLabel.setText(_translate("MainWindow", "EST"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())