#!/usr/bin/python3
# coding: utf8

"""
Global definition of notification messages.
Stored as dictionaries.
"""

BURNER_CONTROLLER_MSGS = {
    "blockage" : "Blocco bruciatore. Pressione minima non rilevata!!!",
    "burner_startup" : "Avviamento bruciatore...controllo incremento di pressione.",
    "temp_reached" : "Il forno ha raggiunto la temperatura impostata. Spegnimento bruciatore."
    }

INTERNAL_OPENING_MSGS = {
    "opening_triggered" : "Apertura interna azionata."
    }

SENS_READER_MSGS = {
    "calibration" : "Avviamento procedura di calibrazione pressione.",
    "startup" : "Avviamento ciclo di lettura sensori.",
    "DB_error" : "Errore nella rilevazione delle temperature."
    }

OVEN_CONTROLLER_MSGS = {
    "burner_blockage" : "Blocco bruciatore causa superamento soglia massima pressione.",
    "valve_on" : "Apertura valvola seconda fiamma.",
    "valve_off" : "Chiusura valvola seconda fiamma.",
    "light_on" : "Accensione luce.",
    "light_off" : "Spegnimento luce.",
    "release_steam" : "Rilascio vapore.",
    "fan_on" : "Ventola bruciatore attiva.",
    "fan_off" : "Ventola bruciatore spenta.",
    "ext_opening_triggered" : "Apertura esterna azionata.",
    "timeout" : "Timer scattato!!!",
    "set_point" : "Nuova temperatura impostata.",
    "function_disabled" : "Funzione disabilitata a bruciatore acceso."
    }