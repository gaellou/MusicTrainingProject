import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget, QPushButton, QRadioButton, QHBoxLayout
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

import sys
import time
import random


import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import sqlite3


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



class SonWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("son.ui", self)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layoutV = QtWidgets.QVBoxLayout(self._main)
        self.setWindowTitle("Son et Musique")

class FourrierWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("fourrier.ui", self)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layoutV = QtWidgets.QVBoxLayout(self._main)
        self.setWindowTitle("Traitement du son")



class PhysicWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(PhysicWindow, self).__init__()

        self.dialogs = list()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layoutV = QtWidgets.QVBoxLayout(self._main)
        self.setWindowTitle("Chauffe")
        self.setGeometry(20, 20, 1000, 1000)

        self.statusBar().showMessage('Ready')  # Faire une barre de status

        buttonSon= QPushButton("Son et Musique", self)
        layoutV.addWidget(buttonSon)
        buttonSon.setStyleSheet("background-color: white")
        buttonSon.clicked.connect(self.SonClicked)

        buttonFourrier= QPushButton("Traitement du son", self)
        layoutV.addWidget(buttonFourrier)
        buttonFourrier.setStyleSheet("background-color: white")
        buttonFourrier.clicked.connect(self.FourrierClicked)

        Instlayout = QHBoxLayout() #creer un calque "honrizontal"
        Instlayout.addWidget(buttonSon) # et ajoute lui un widget ici un bouton
        Instlayout.addWidget(buttonFourrier)

        layoutV.addLayout(Instlayout)
        Boutongraph1 = QPushButton("Partition",self) # creer un bouton à l'écran oK mais cela ne dit pas ou
        layoutV.addWidget(Boutongraph1) # ce bouton met le dans le calque layoutV maintenant je sais ou est le bouton
        Boutongraph1.clicked.connect(self.plotImage)
        Boutongraph2 = QPushButton("Courbe",self)
        layoutV.addWidget(Boutongraph2)
        Boutongraph2.clicked.connect(self.sinusoiddynamyque)

        Hlayout = QHBoxLayout() #creer un calque "honrizontal"
        Hlayout.addWidget(Boutongraph1) # et ajoute lui un widget ici un bouton
        Hlayout.addWidget(Boutongraph2) # et ajoutes lui un  2 ème bouton

        layoutV.addLayout(Hlayout)  # et ajoute le Hlayout dans le Layout vertical

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))  # creer un canevas
        layoutV.addWidget(static_canvas) # et mets le dans le layoutV

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))  # creer un 2 ème canevas
        layoutV.addWidget(dynamic_canvas) # et met le aussi dans le layoutV
        ToolBar2 = NavigationToolbar(dynamic_canvas, self)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,ToolBar2)
        layoutV.addWidget(ToolBar2) #et le met la NavigationToolbar sur le layout qui va bien



        self._static_ax = static_canvas.figure.add_subplot(111)  # cette ligne ne pouvais pas être mis dans la fonction graphstatic sinon le bouton n'afficher pas le graphique  ce sont les axes du premier canevas appeler static_canvas



        self._dynamic_ax = dynamic_canvas.figure.add_subplot(111) # creer les axes du 2 ème canevas le canevas dynamique
        #self._timer = dynamic_canvas.new_timer(100, [(self._update_canvas, (), {})])
        #self._timer.start()   # fonctionne mais sans le déclenchement du bouton


    def graphstatic(self,static_canvas):  # il fallait aussi transmettre le 2 ème paramètre static_canvas à la fonction graphstatic
        img = mpimg.imread('./Partition/Exo01_1.png')
        print(img)
        imgplot = plt.imshow(img)
        self.axescanvas3.imshow(img)
        self.axescanvas3.set_title('PyQt Matplotlib Example')
        self.axescanvas3.figure.canvas.draw()

    def sinusoiddynamyque(self):

        testhopbof = FigureCanvas(Figure(figsize=(5, 3)))

        self._timer = testhopbof.new_timer(100, [(self._update_canvas, (), {})])   #ne fonctionne pas car new_timer n'est pas détecté problème de portée ?
        self._timer.start()


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

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()

    def plotImage(self,canvas3):
        NomFichier = './IMAGE/Exercices/Ex12.png'
        img = mpimg.imread(NomFichier)
        #print(img)
        imgplot = plt.imshow(img)
        self._static_ax .imshow(img)
        self._static_ax.set_title('PyQt Matplotlib Example')
        self._static_ax .figure.canvas.draw()

    def SonClicked(self) :

        dialogSon = SonWindow(self)
        self.dialogs.append(dialogSon)
        dialogSon.show()
        print("Son et Musique")

    def FourrierClicked(self) :
        dialogFour = FourrierWindow(self)
        self.dialogs.append(dialogFour)
        dialogFour.show()

        print("Traitement du son")




class SolfegeWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("solfege.ui", self)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layoutV = QtWidgets.QVBoxLayout(self._main)
        self.setWindowTitle("Mémo de Solfège")



class TraningWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TraningWindow, self).__init__()

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layoutV = QtWidgets.QVBoxLayout(self._main)
        self.setWindowTitle("Entrainement")
        self.setGeometry(20, 20, 1000, 1000)

        self.statusBar().showMessage('Ready')  # Faire une barre de status

        buttonFlute= QPushButton("Flute", self)
        layoutV.addWidget(buttonFlute)
        buttonFlute.setStyleSheet("background-color: white")
        buttonFlute.clicked.connect(self.FluteClicked)

        buttonTrumpet= QPushButton("Trompette", self)
        layoutV.addWidget(buttonTrumpet)
        buttonTrumpet.setStyleSheet("background-color: white")
        buttonTrumpet.clicked.connect(self.TrumpetClicked)

        buttonViolin= QPushButton("Violin", self)
        layoutV.addWidget(buttonViolin)
        buttonViolin.setStyleSheet("background-color: white")
        buttonViolin.clicked.connect(self.ViolinClicked)

        buttonClarinet= QPushButton("Clarinette", self)
        layoutV.addWidget(buttonClarinet)
        buttonClarinet.setStyleSheet("background-color: white")
        buttonClarinet.clicked.connect(self.ClarinetClicked)

        Instlayout = QHBoxLayout() #creer un calque "honrizontal"
        Instlayout.addWidget(buttonTrumpet) # et ajoute lui un widget ici un bouton
        Instlayout.addWidget(buttonFlute)
        Instlayout.addWidget(buttonViolin)
        Instlayout.addWidget(buttonClarinet)

        layoutV.addLayout(Instlayout)

        Boutongraph1 = QPushButton("Partition",self) # creer un bouton à l'écran oK mais cela ne dit pas ou
        layoutV.addWidget(Boutongraph1) # ce bouton met le dans le calque layoutV maintenant je sais ou est le bouton
        Boutongraph1.clicked.connect(self.plotImage)
        Boutongraph2 = QPushButton("Courbe",self)
        layoutV.addWidget(Boutongraph2)
        Boutongraph2.clicked.connect(self.sinusoiddynamyque)

        Hlayout = QHBoxLayout() #creer un calque "honrizontal"
        Hlayout.addWidget(Boutongraph1) # et ajoute lui un widget ici un bouton
        Hlayout.addWidget(Boutongraph2) # et ajoutes lui un  2 ème bouton

        layoutV.addLayout(Hlayout)  # et ajoute le Hlayout dans le Layout vertical

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))  # creer un canevas
        layoutV.addWidget(static_canvas) # et mets le dans le layoutV

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))  # creer un 2 ème canevas
        layoutV.addWidget(dynamic_canvas) # et met le aussi dans le layoutV
        ToolBar2 = NavigationToolbar(dynamic_canvas, self)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,ToolBar2)
        layoutV.addWidget(ToolBar2) #et le met la NavigationToolbar sur le layout qui va bien



        self._static_ax = static_canvas.figure.add_subplot(111)  # cette ligne ne pouvais pas être mis dans la fonction graphstatic sinon le bouton n'afficher pas le graphique  ce sont les axes du premier canevas appeler static_canvas



        self._dynamic_ax = dynamic_canvas.figure.add_subplot(111) # creer les axes du 2 ème canevas le canevas dynamique
        #self._timer = dynamic_canvas.new_timer(100, [(self._update_canvas, (), {})])
        #self._timer.start()   # fonctionne mais sans le déclenchement du bouton


    def graphstatic(self,static_canvas):  # il fallait aussi transmettre le 2 ème paramètre static_canvas à la fonction graphstatic
        img = mpimg.imread('./Partition/Exo01_1.png')
        print(img)
        imgplot = plt.imshow(img)
        self.axescanvas3.imshow(img)
        self.axescanvas3.set_title('PyQt Matplotlib Example')
        self.axescanvas3.figure.canvas.draw()

    def sinusoiddynamyque(self):

        testhopbof = FigureCanvas(Figure(figsize=(5, 3)))

        self._timer = testhopbof.new_timer(100, [(self._update_canvas, (), {})])   #ne fonctionne pas car new_timer n'est pas détecté problème de portée ?
        self._timer.start()


    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()

    def plotImage(self,canvas3):
        NomFichier = './IMAGE/Exercices/Ex12.png'
        img = mpimg.imread(NomFichier)
        #print(img)
        imgplot = plt.imshow(img)
        self._static_ax .imshow(img)
        self._static_ax.set_title('PyQt Matplotlib Example')
        self._static_ax .figure.canvas.draw()

    def TrumpetClicked(self) :

        print("Instrument : Trompette")

    def FluteClicked(self) :

        print("Instrument : Flute")
    def ViolinClicked(self) :

        print("Instrument : Violon")
    def ClarinetClicked(self) :

        print("Instrument : Clarinette")

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ApplicationWindow, self).__init__()

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layoutV = QtWidgets.QVBoxLayout(self._main)
        self.setWindowTitle("Chauffe")
        self.setGeometry(20, 20, 1000, 1000)

        self.statusBar().showMessage('Ready')  # Faire une barre de status

        buttonFlute= QPushButton("Flute", self)
        layoutV.addWidget(buttonFlute)
        buttonFlute.setStyleSheet("background-color: white")
        buttonFlute.clicked.connect(self.FluteClicked)

        buttonTrumpet= QPushButton("Trompette", self)
        layoutV.addWidget(buttonTrumpet)
        buttonTrumpet.setStyleSheet("background-color: white")
        buttonTrumpet.clicked.connect(self.TrumpetClicked)

        buttonViolin= QPushButton("Violin", self)
        layoutV.addWidget(buttonViolin)
        buttonViolin.setStyleSheet("background-color: white")
        buttonViolin.clicked.connect(self.ViolinClicked)

        buttonClarinet= QPushButton("Clarinette", self)
        layoutV.addWidget(buttonClarinet)
        buttonClarinet.setStyleSheet("background-color: white")
        buttonClarinet.clicked.connect(self.ClarinetClicked)

        Instlayout = QHBoxLayout() #creer un calque "honrizontal"
        Instlayout.addWidget(buttonTrumpet) # et ajoute lui un widget ici un bouton
        Instlayout.addWidget(buttonFlute)
        Instlayout.addWidget(buttonViolin)
        Instlayout.addWidget(buttonClarinet)

        layoutV.addLayout(Instlayout)
        Boutongraph1 = QPushButton("Partition",self) # creer un bouton à l'écran oK mais cela ne dit pas ou
        layoutV.addWidget(Boutongraph1) # ce bouton met le dans le calque layoutV maintenant je sais ou est le bouton
        Boutongraph1.clicked.connect(self.plotImage)
        Boutongraph2 = QPushButton("Courbe",self)
        layoutV.addWidget(Boutongraph2)
        Boutongraph2.clicked.connect(self.sinusoiddynamyque)

        Hlayout = QHBoxLayout() #creer un calque "honrizontal"
        Hlayout.addWidget(Boutongraph1) # et ajoute lui un widget ici un bouton
        Hlayout.addWidget(Boutongraph2) # et ajoutes lui un  2 ème bouton

        layoutV.addLayout(Hlayout)  # et ajoute le Hlayout dans le Layout vertical

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))  # creer un canevas
        layoutV.addWidget(static_canvas) # et mets le dans le layoutV

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))  # creer un 2 ème canevas
        layoutV.addWidget(dynamic_canvas) # et met le aussi dans le layoutV
        ToolBar2 = NavigationToolbar(dynamic_canvas, self)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,ToolBar2)
        layoutV.addWidget(ToolBar2) #et le met la NavigationToolbar sur le layout qui va bien



        self._static_ax = static_canvas.figure.add_subplot(111)  # cette ligne ne pouvais pas être mis dans la fonction graphstatic sinon le bouton n'afficher pas le graphique  ce sont les axes du premier canevas appeler static_canvas



        self._dynamic_ax = dynamic_canvas.figure.add_subplot(111) # creer les axes du 2 ème canevas le canevas dynamique
        #self._timer = dynamic_canvas.new_timer(100, [(self._update_canvas, (), {})])
        #self._timer.start()   # fonctionne mais sans le déclenchement du bouton


    def graphstatic(self,static_canvas):  # il fallait aussi transmettre le 2 ème paramètre static_canvas à la fonction graphstatic
        img = mpimg.imread('./Partition/Exo01_1.png')
        print(img)
        imgplot = plt.imshow(img)
        self.axescanvas3.imshow(img)
        self.axescanvas3.set_title('PyQt Matplotlib Example')
        self.axescanvas3.figure.canvas.draw()

    def sinusoiddynamyque(self):

        testhopbof = FigureCanvas(Figure(figsize=(5, 3)))

        self._timer = testhopbof.new_timer(100, [(self._update_canvas, (), {})])   #ne fonctionne pas car new_timer n'est pas détecté problème de portée ?
        self._timer.start()


    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()

    def plotImage(self,canvas3):
        NomFichier = './IMAGE/Exercices/Ex12.png'
        img = mpimg.imread(NomFichier)
        #print(img)
        imgplot = plt.imshow(img)
        self._static_ax .imshow(img)
        self._static_ax.set_title('PyQt Matplotlib Example')
        self._static_ax .figure.canvas.draw()

    def TrumpetClicked(self) :


        print("Instrument : Trompette")

    def FluteClicked(self) :


        print("Instrument : Flute")
    def ViolinClicked(self) :


        print("Instrument : Violon")
    def ClarinetClicked(self) :


        print("Instrument : Clarinette")



class MainWindow(QtWidgets.QMainWindow):

#variables
    Diapason = 440
    FréqLaInst = Diapason #dépend de l'instrument choisi
    Tempo = 85


    def WarmUpClicked(self) :
        dialog = ApplicationWindow(self)
        self.dialogs.append(dialog)
        dialog.show()


    def PracticeClicked(self) :
        dialog = TraningWindow(self)
        self.dialogs.append(dialog)
        dialog.show()




    def SolfegeClicked(self) :
        dialog = SolfegeWindow(self)
        self.dialogs.append(dialog)
        dialog.show()


    def PhysicClicked(self) :
        dialog = PhysicWindow(self)
        self.dialogs.append(dialog)
        dialog.show()

    def ChangeDiapason(self, CheckBox, Diapason) :
        pass



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)


        self.dialogs = list()

        buttonWarmUp= QPushButton("Je chauffe", self)
        buttonWarmUp.move(90,500)
        buttonWarmUp.setFixedHeight(50)
        buttonWarmUp.setStyleSheet("background-color: white")
        buttonWarmUp.clicked.connect(self.WarmUpClicked)

        buttonPractice= QPushButton("Je m'entraine", self)
        buttonPractice.move(430,500)
        buttonPractice.setFixedHeight(50)
        buttonPractice.setStyleSheet("background-color: white")
        buttonPractice.clicked.connect(self.PracticeClicked)

        buttonSolfege= QPushButton("Mémo de Solfège", self)
        buttonSolfege.move(790,500)
        buttonSolfege.setFixedHeight(50)
        buttonSolfege.setFixedWidth(125)
        buttonSolfege.setStyleSheet("background-color: white")
        buttonSolfege.clicked.connect(self.SolfegeClicked)


        buttonPhysic= QPushButton("Physique du son", self)
        buttonPhysic.move(1100,500)
        buttonPhysic.setFixedHeight(50)
        buttonPhysic.setFixedWidth(125)
        buttonPhysic.setStyleSheet("background-color: white")
        buttonPhysic.clicked.connect(self.PhysicClicked)





class Canvas(FigureCanvas): #trace la figure matplot dans la fenêtre
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(111)


        FigureCanvas.__init__(self, fig)

        self.setParent(parent)


        self.plot()


    def plot(self): #donne la figure

        x = np.array([50, 30,40])

        labels = ["Apples", "Bananas", "Melons"]

        ax = self.figure.add_subplot(111)

        ax.pie(x, labels=labels)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()


