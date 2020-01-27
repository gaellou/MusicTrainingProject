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

def normaliser_son_mono(x):
    M = np.max(abs(x)); ## la plus grande valeur absolue du signal
    return  x/M;

def file(name_file,signal,rate):
    signal = 0.7*normaliser_son_mono(signal)  ##pour protéger vos oreilles des saturations de vos enceintes 
    scaled = np.round(32767*signal)
    signal = scaled.astype(np.int16)
    io.write(name_file, rate, signal)
    
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

dureeChunk = 0.1
RATE = 44100   #frequence d'échantillonage
CHUNK = int(dureeChunk *RATE) #longeur du tronçons de donnée à analyser, plus grand plus fft precise
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEUIL = 15 #pour afficher le seuil,  en dB 
#PAS = 1024 * 4 # troncons que traite effectivemnt la fft avec nfft


fe = 44100  
te = 1/fe
t= np.arange(0, 5, te)


p = pyaudio.PyAudio()

#data du micro
stream = p.open(
    format = FORMAT ,
    channels = CHANNELS,
    rate = RATE,
    input= True,
    output = True,
    frames_per_buffer=CHUNK)

total_data = []
nb_s = 2
for k in range(15*nb_s):
    data = stream.read(CHUNK)#data en binaire
    data_int = np.array(struct.unpack(str(2*CHUNK)+ 'B', data),dtype='b')[::2] -127 /128
    total_data = np.append(total_data,data_int)
    print(k)

i = 5
plt.plot(total_data)
name = 'enregistrement_audio_numero' + str(i) +'.wav'
print(name)
file(name,total_data,44100)


rate, data = io.read(name) ## importer le fichier son*
CHUNK1 = data
freq , periodo1 = calcul_periodogramme1(CHUNK1, RATE)
plt.figure(figsize= (15,10))
plt.plot(freq, periodo1)
plt.xlim(0,5000)
plt.ylim(-150,150)