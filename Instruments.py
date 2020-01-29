# -*- coding: utf-8 -*-

try:
    from PySide import QtWidgets
except:
    from PyQt5 import QtWidgets


class Instruments:
    Nom = 'Nom'
    NoteBasse = 0 #numero MIDI
    NoteHaute = 0 #Numéro MIDI
    Clef = 'clé' #violin, french, alto, bass
    Diapasion = 440 #frequence
    Pmax = 1 #float
    Pmin = 1 #float

    def étalonage() :
        #code
