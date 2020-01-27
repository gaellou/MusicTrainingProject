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
import time


from scipy import signal
import os
%matplotlib tk

def calcul_periodogramme1(x,Fe):
    ### périodogramme moyenné. Sections de 0.1 seconde
    N=len(x)
   # N1=int(np.floor(Fe))
   # K=int(np.floor(N))
    w=signal.hamming(N)
    b = w* x
    f, B = signal.periodogram(b, Fe,nfft =44100)
    B = B/N
    B=10*np.log10(B)
    return(f,B)


def affiche_perido():
	RATE = 44100 
	rate, data = io.read('TEST CLARINET.wav') ## importer le fichier son*
	duree = 0.2
	D =int (duree * RATE) #nb ech d'1 bloc
	t_in1 =1 
	n1 = int(t_in1*RATE)
	CHUNK1 = data[n1:(n1+D),0]
	freq , periodo1 = calcul_periodogramme1(CHUNK1, RATE) 
	plt.figure(figsize= (15,10))
	plt.plot(freq, periodo1)
	plt.xlim(0,250)
	plt.ylim(-150,150)
	return 0



