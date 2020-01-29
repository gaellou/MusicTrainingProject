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
%matplotlib tk
#####
dureeChunk = 0.1
RATE = 44100   #frequence d'échantillonage
CHUNK = int(dureeChunk *RATE) #longeur du tronçons de donnée à analyser, plus grand plus fft precise
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEUIL = 15 #pour afficher le seuil,  en dB 
#####
alpha = 2**(1/12) #pas pour la gamme tempérée
note_grave = 220
Nb_Octave = 1
OCTAVE = np.zeros(13*Nb_Octave)
for i in range (13*Nb_Octave):
    OCTAVE[i]= note_grave*(alpha**i)
#####   
Freq_Min =note_grave #affichage de la freq min pour le temps-freq
Freq_Max = note_grave*(2**Nb_Octave)  #affichage de la freq max pour le temps-freq
#####
freq_min_recherche = 220
freq_max_recherche = 440
#####
TimeListen = 30 #largeur aproximatif d'écoute en s de l'analyse temps-freq

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

def Energie(x):
    E = 0
    for k in range(len(x)-1):
        E+=(x[k]**2)
    return 10*np.log10(E/len(x))

def stream_audio(self):
    p = pyaudio.PyAudio()
    #data du micro
    stream = p.open(
        format = FORMAT ,
        channels = CHANNELS,
        rate = RATE,
        input= True,
        output = True,
        frames_per_buffer=CHUNK)
    #######
    fig, (ax,ax_fft,ax2) = plt.subplots(3,figsize=(10,7))
    #######
    ax.set_xlim(0,CHUNK)
    ax_fft.set_xlim(0,RATE/20)
    ax2.set_xlim(0,TimeListen*7.5)
    axK = ax2
    #######
    #variable pour plotter
    x = np.arange(0, 1 * CHUNK ,1)
    x2 = np.arange(0,1*CHUNK,1)
    xK = np.arange(0, 1*CHUNK ,1)
    x_fft, aux = calcul_periodogramme(np.zeros(CHUNK),RATE,0.1)
    #######
    line, = ax.plot(x,np.random.rand(CHUNK),'-',lw=2)
    line_x_fft, = ax_fft.plot((x_fft),np.random.rand(len(x_fft)),'-',lw=2)
    line_x2, = ax2.plot(x2,np.random.rand(CHUNK),'-',lw=2)
    lineK, = axK.plot(xK,np.random.rand(CHUNK),'-',lw=2)
    #######
    ax.set_title("AUDIO FORME D'ONDE")
    ax.set_ylabel('volume')
    ax.set_ylim(-128,128)
    #######
    ax_fft.set_title("AUDIO SPECTRE")
    ax_fft.set_ylabel('Amplitude')
    ax_fft.set_ylim(-100,25)
    #ax_fft.set_xlim(0.001,CHUNK)
    ########
    plt.grid()
    ax2.set_ylim(Freq_Min,Freq_Max)
    ax2.set_title("ANALYSE FREQ/TEMPS")
    ax2.set_ylabel('freq')
    plt.yticks(OCTAVE, ["La", "Sib", "Si","Do","Do#","Ré","Mib","Mi","Fa","Fa#","Sol","Sol#","La" ]*Nb_Octave)
    ########
    axK.set_ylim(Freq_Min,Freq_Max)
    axK.set_title("KARAOKE FREQ/TEMPS")
    axK.set_ylabel('freq')
    plt.yticks(OCTAVE, ["La", "Sib", "Si","Do","Do#","Ré","Mib","Mi","Fa","Fa#","Sol","Sol#","La" ]*Nb_Octave)
    ########
    m = np.zeros(CHUNK)
    i = 10
    ########
    liste_test_indice = [5,7,9,10,9,7]
    liste_test_valeur = [4,8,8,4,4,1]
    #liste_test_indice = [0,5,0]
    #liste_test_valeur = [8,8,8]
    ########
    Tau = 20
    Pause = 10
    ########
    ka =  np.zeros(CHUNK)
    karao = np.append(son_et_affiche_karaoke('gamme_test147.wav',liste_test_indice,0,liste_test_valeur,60),np.zeros(Pause))
    for j in range(5):
        karao = np.append(karao,karao)
    marche = False
    ########
    while True:
        data = stream.read(CHUNK)#data en binaire
        data_int = np.array(struct.unpack(str(2*CHUNK)+ 'B', data),dtype='b')[::2] 
        line.set_ydata(data_int)
        #########
        for j in range (len(karao)-1):
            ka[j+Tau]= karao[j]
        lineK.set_ydata(ka)
        #########
        freq , periodo = calcul_periodogramme(data_int,RATE,0.1)
        line_x_fft.set_ydata(periodo) 
        #########
        NRJ = Energie(data_int)
        if(NRJ>SEUIL_HAUT or (marche==True)):
            marche = True
            if(NRJ < SEUIL_BAS):
                m[i]=0
            else:
                cond = (freq >freq_min_recherche) * (freq <freq_max_recherche)
                periodo2 = (periodo+100)*cond
                ma = np.argmax(periodo2)
                pitch = freq[ma]
                m[i]= ma
            ########
            line_x2.set_ydata(m)
            ax2.set_xlim(left = max (0, i-25), right = i+25)
        #########
        if(marche==True):
            i+=1
        try:
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

        except tkinter.TclError:
            break

    
        