#!/usr/bin/python3
# coding: utf8

"""
Global definition of pin numbers.
"""

# Serial Clock (shared between thermocouples)
CLK = 21

# First thermocouple - Chip Select and Serial Output
CS1  = 12
SO1  = 5

# Second thermocouple - Chip Select and Serial Output
CS2  = 6
SO2  = 13

# Third thermocouple - Chip Select and Serial Output
CS3  = 16
SO3  = 20

# Fourth thermocouple - Chip Select and Serial Output
CS4  = 19
SO4  = 26

####  Relay GPIO  ####

# GPIO | Relay
#--------------
# 04     01
# 17     02
# 18     03
# 27     04
# 22     05
# 23     06
# 24     07
# 25     08

RELAY1_BURNER = 4
RELAY2_BURNER_VALVE = 17
RELAY3_BURNER_FAN = 18
RELAY4_LIGHT = 27
RELAY5_STEAM = 22
RELAY6_INT_OPENING = 23
RELAY7_EST_OPENING = 24
RELAY8_RPI_FAN = 25

# GPIO | Relay
#--------------
# 14     09
# 15     10
# 08     11
# 07     12   unused

RELAY9_ROTISSERIE = 14
RELAY10_RESISTANCE = 15
RELAY11_VACUUM = 8
RELAY12_UNUSED = 7