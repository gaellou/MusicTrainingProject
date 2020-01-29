# -*- coding: utf-8 -*-

import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
import tkinter
from scipy.fftpack import fft
from scipy.fftpack import rfft
from scipy.io import wavfile as io
from playsound import playsound
from tempfile import TemporaryFile
from scipy import signal
import os

from PyQt5 import QtCore, QtGui, QtWidgets
try:
    from PySide import QtWidgets
except:
    from PyQt5 import QtWidgets


class DataGeneration:

    new_data=QtCore.pyqtSignal()


    def __init__(self):
        super().init(parent)
    def data_generation(self):

        while True :
            pass


class KaraokePlot :
    new_data=QtCore.pyqtSignal()
    def __init__(self) :
        super().init(parent)
    def calcul_periodogramme(x,Fe,duree_sous_bloc):
         ### périodogramme moyenné. Sections de 0.1 seconde
        N=len(x)
        N1=int(np.floor(duree_sous_bloc*Fe))
        K=int(np.floor(N/N1))
        w=signal.hamming(N1)
        ind1 = 0
        ind2 = N1-1
        b = w*x[ind1:(ind2+1)]
        f, B = signal.periodogram(b, Fe,nfft =44100)
        B=B/N1
        while ind2+N1<N:
            ind1=ind1+N1
            ind2=ind2+N1
            b=w*x[ind1:(ind2+1)]
            f, aux = signal.periodogram(b, Fe, nfft =44100)
            B=B+aux/N1
        B=B/K
        B[0]=0.1
        B=10*np.log10(B+0.000000001)
        return(f,B)

    def normaliser_son_mono(x):
        M = np.max(abs(x)); ## la plus grande valeur absolue du signal
        return  x/M;

    def file(name_file,signal,rate):
        signal = 0.5*normaliser_son_mono(signal)  ##pour protéger vos oreilles des saturations de vos enceintes
        scaled = np.round(32767*signal)
        signal = scaled.astype(np.int16)
        io.write(name_file, rate, signal)

    def son(f0,durée_note):
        fe = 44100
        te = 1/fe
        t= np.arange(0, durée_note, te)
        return np.cos(2*(np.pi)*f0*t)*2* np.sin(t*(np.pi)/durée_note)

    def Gamme_temperée(Nb_Octave, note_fondamental):
        alpha = 2**(1/12)

        OCTAVE = np.zeros(1+12*Nb_Octave)

        for i in range (1+12*Nb_Octave):

            OCTAVE[i]= note_fondamental*(alpha**i)

        return OCTAVE

    def creation_liste_note(fondamental_gamme, liste_indice_note):
        gamme = Gamme_temperée(2,fondamental_gamme)
        res =  np.zeros(len(liste_indice_note))
        for k in range (len(liste_indice_note)):
            res[k]= gamme[liste_indice_note[k]]
        return res

    def suite_note(liste_note,liste_duree_note):
        fe = 44100
        te = 1/fe
        x_total = []

        for i in range (len(liste_note)):
            t= np.arange(0, liste_duree_note[i], te)
            x_tampon = son(liste_note[i],liste_duree_note[i])
            x_total = np.concatenate((x_total,x_tampon))
        somme_duree_note = 0
        for k in range (len(liste_duree_note)):
            somme_duree_note += liste_duree_note[k]
        time = np.arange(0,somme_duree_note,te)
        return x_total

    def creer_fichier(file_name , suiteNote):
        file(file_name,suiteNote,44100)

    def creation_duree(liste_valeur,tempo):
        FreqNOIRE = tempo/60 #Hz
        d_NOIRE = 1/FreqNOIRE
        duree_note = []
        duree_note[:] = [4*d_NOIRE/x for x in liste_valeur]
        return duree_note

    def karaoke(liste_note, liste_valeur,tempo):
        liste_note = creation_liste_note(220,liste_note)
        liste_duree = creation_duree(liste_valeur,tempo)
        duree_total = sum(liste_duree)*RATE
        kara = []
        for k in range (len(liste_duree)):
            for i in range(int((liste_duree[k])*(60/tempo))):
                kara.append(liste_note[k])
        return kara

    def son_et_affiche_karaoke(fileName,liste_note,transposition, liste_valeur,tempo):
        liste_note = [x + transposition for x in liste_note]
        liste_duree = creation_duree(liste_valeur,tempo)
        liste_note_son = creation_liste_note(220,liste_note)
        suiteNote = suite_note(liste_note_son,liste_duree)
        karao = karaoke(liste_note,liste_duree,tempo)
        fichier_son = creer_fichier(fileName,suiteNote)
        playsound(fileName)

        return karao
