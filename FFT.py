#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import signal
#%matplotlib tk

CHUNK = 1024 * 4 #longeur du tronçons de donnée à analyser, plus grand plus fft precise
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100   #frequence d'échantillonage
SEUIL = 100 #pour afficher le seuil, 125 est le max
PAS = 1024 * 4 # troncons que traite effectivemnt la fft avec nfft

alpha = 2**(1/12) #pas pour la gamme tempérée
note_grave = 880
Nb_Octave = 1
OCTAVE = np.zeros(13*Nb_Octave)
for i in range (13*Nb_Octave):
    OCTAVE[i]= note_grave*(alpha**i)

Freq_Min = note_grave #affichage de la freq min pour le temps-freq
Freq_Max = note_grave*(2**Nb_Octave)  #affichage de la freq max pour le temps-freq
TimeListen = 20 #largeur aproximatif d'écoute en s de l'analyse temps-freq

p = pyaudio.PyAudio()

#data du micro
stream = p.open(
    format = FORMAT ,
    channels = CHANNELS,
    rate = RATE,
    input= True,
    output = True,
    frames_per_buffer=CHUNK)



fig, (ax,ax_fft,ax2) = plt.subplots(3,figsize=(10,7))
ax.set_xlim(0,CHUNK)
ax2.set_xlim(0,20*TimeListen)
ax_fft.set_xlim(0,RATE/20)


#variable pour plotter
x = np.arange(0, 1 * CHUNK ,1)
x2 = np.arange(0,1*CHUNK,1)

x_fft, aux = signal.periodogram(np.zeros(CHUNK),RATE,nfft=PAS)


line, = ax.plot(x,np.random.rand(CHUNK),'-',lw=2)
line_x2, = ax2.plot(x2,np.random.rand(CHUNK),'-',lw=2)
line_x_fft, = ax_fft.plot((x_fft),np.random.rand(len(x_fft)),'-',lw=2)
#plt.setp(ax_fft,xticks=[55,110,220,440,880,1760,3560])


ax.set_title("AUDIO FORME D'ONDE")

ax.set_ylabel('volume')
ax.set_ylim(-150,150)
#ax.set_xlim(0,CHUNK)


ax_fft.set_title("AUDIO SPECTRE")
ax_fft.set_ylabel('Amplitude')
ax_fft.set_ylim(0,10)
#ax_fft.set_xlim(0.001,CHUNK)


ax2.set_title("ANALYSE FREQ/TEMPS")
ax2.set_ylabel('freq')
plt.yticks(OCTAVE, ["La", "Sib", "Si","Do","Do#","Ré","Mib","Mi","Fa","Fa#","Sol","Sol#","La" ]*Nb_Octave)
ax2.set_ylim(Freq_Min,Freq_Max)


m = np.zeros(CHUNK)
i = 0

fenetre = signal.get_window('hamming',PAS)

while True:

    data = stream.read(CHUNK)#data en binaire
    data_int = np.array(struct.unpack(str(2*CHUNK)+ 'B', data),dtype='b')[::2]
    line.set_ydata(data_int)

    if(np.max(data_int)>SEUIL):
        print("depasse le seuil")

    aux , y_fft = signal.periodogram(data_int-128,RATE,fenetre,nfft=PAS)
    line_x_fft.set_ydata((y_fft))
    #print(len(y_fft))

    ma=(np.argmax(np.abs(y_fft[100:]))+100)
    m[i]= ma
    print(m[i])
    i= i+1

    line_x2.set_ydata(m)
    fig.canvas.draw()
    fig.canvas.flush_events()
print(len (y_fft))
