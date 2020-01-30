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

def calcul_periodogramme2(x,Fe,duree_sous_bloc):
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
    B=10*np.log10(B)
    return(f,B)


def Affiche_periodo_et_harmoniques(fileName, freq_min_recherche,freq_max_recherche):
    rate, data = io.read(fileName) ## importer le fichier son*
    freq , periodo1 = calcul_periodogramme2(data, 44100, 0.05)
    cond = (freq >freq_min_recherche) * (freq <freq_max_recherche)
    periodo2 = (periodo1+200)*cond
    m = np.argmax(periodo2)
    print('TRACE OK')
    A = []

    return (freq , periodo1)



