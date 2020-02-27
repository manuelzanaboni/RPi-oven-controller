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

# change names?
RELAY1 = 4
RELAY2 = 17
RELAY3 = 18
RELAY4 = 27
RELAY5 = 22
RELAY6 = 23
RELAY7 = 24
RELAY8 = 25