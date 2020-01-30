import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
import tkinter
from scipy.fftpack import fft
from scipy.fftpack import rfft
from scipy.io import wavfile as io
from tempfile import TemporaryFile
import time
#from pydub import AudioSegment
#from pydub.playback import play
from scipy import signal
import os
import math as math

from periodo import *
################
dureeChunk = 0.1
RATE = 44100   #frequence d'échantillonage
CHUNK = int(dureeChunk *RATE) #longeur du tronçons de donnée à analyser, plus grand plus fft precise
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEUIL = 15 #pour afficher le seuil,  en dB 
nb_s = 3
freq_min_recherche = 150
freq_max_recherche = 500 
Te = 1/RATE

#####################

def normaliser_son_mono(x):
    M = np.max(abs(x)); ## la plus grande valeur absolue du signal
    return  x/M;

def convertir_wav(name_file,signal,rate):
    signal = 0.7*normaliser_son_mono(signal)  ##pour protéger vos oreilles des saturations de vos enceintes 
    scaled = np.round(32767*signal)
    signal = scaled.astype(np.int16)
    io.write(name_file, rate, signal)

def enregistrer_static(namefile,temps_acquisition):
    total_data = []
    p = pyaudio.PyAudio()
        #data du micro

    stream = p.open(

    format = FORMAT ,

    channels = CHANNELS,

    rate = RATE,

    input= True,

    output = True,

    frames_per_buffer=CHUNK)

    for k in range(10*temps_acquisition):

        data = stream.read(CHUNK)#data en binaire

        data_int = np.array(struct.unpack(str(2*CHUNK)+ 'B', data),dtype='b')[::2] -127 /128

        total_data = np.append(total_data,data_int)
    t = np.arange(0,temps_acquisition,Te)

    convertir_wav(namefile,total_data,RATE)

    return total_data


def Energie(x):
    E = 0
    for k in range(len(x)-1):
        E+=(x[k]**2)
    return 10*np.log10(E/len(x))


def declancheur_seuil(SEUIL,namefile):
    marche = False
    total_data = []
    p = pyaudio.PyAudio()
    #data du micro
    stream = p.open(
        format = FORMAT ,
        channels = CHANNELS,
        rate = RATE,
        input= True,
        output = True,
        frames_per_buffer=CHUNK)
    while True:
        data = stream.read(CHUNK)#data en binaire
        data_int = np.array(struct.unpack(str(2*CHUNK)+ 'B', data),dtype='b')[::2] -127 /128
        NRJ = Energie(data_int)
        print(NRJ)
        if (NRJ>SEUIL):
            total_data = np.append(total_data,data_int)
            marche = True
        if ((marche ==True) and (NRJ<2*SEUIL/3)):
            convertir_wav(namefile,total_data,RATE)
            return (total_data)


