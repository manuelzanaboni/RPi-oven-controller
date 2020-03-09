#!/usr/bin/python3
# coding: utf8

"""
Global definition of notification messages.
Stored as dictionaries.
"""

BURNER_CONTROLLER_MSGS = {}

INTERNAL_OPENING_MSGS = {
    "opening_triggered" : "Apertura interna azionata."
    }

RPI_FAN_MSGS = {
    "fan_on" : "Ventola di raffrescamento attivata.",
    "fan_off" : "Ventola di raffrescamento disattivata."
    }

SENS_READER_MSGS = {
    "calibration" : "Avviamento procedura di calibrazione pressione.",
    "startup" : "Avviamento ciclo di lettura sensori."
    }

OVEN_CONTROLLER_MSGS = {
    "burner_blockage" : "Blocco bruciatore causa superamento massima soglia pressione.",
    "valve_on" : "Apertura valvola seconda fiamma.",
    "valve_off" : "Chiusura valvola seconda fiamma.",
    "light_on" : "Accensione luce.",
    "light_off" : "Spegnimento luce.",
    "release_steam" : "Rilascio vapore.",
    "fan_on" : "Ventola bruciatore attivata.",
    "fan_off" : "Ventola bruciatore disattivata.",
    "ext_opening_triggered" : "Apertura esterna azionata.",
    "timeout" : "Timer scattato!!!",
    "set_point" : "Nuova temperatura impostata."
    }