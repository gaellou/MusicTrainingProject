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

from periodo import *

from enregistrement_static import *


class RecordWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(RecordWindow, self).__init__()

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layoutV = QtWidgets.QVBoxLayout(self._main)
        self.setWindowTitle("Entrainement")
        self.setGeometry(20, 20, 1000, 1000)

        self.statusBar().showMessage('Ready')  # Faire une barre de status

        buttonRecord01= QPushButton("Enregistrer premier son", self)
        layoutV.addWidget(buttonRecord01)
        buttonRecord01.setStyleSheet("background-color: white")
        buttonRecord01.clicked.connect(self.Record01Clicked)

        buttonRecord02= QPushButton("Enregistrer second son", self)
        layoutV.addWidget(buttonRecord02)
        buttonRecord02.setStyleSheet("background-color: white")
        buttonRecord02.clicked.connect(self.Record02Clicked)

        Instlayout = QHBoxLayout() #creer un calque "honrizontal"
        Instlayout.addWidget(buttonRecord01) # et ajoute lui un widget ici un bouton
        Instlayout.addWidget(buttonRecord02)


        layoutV.addLayout(Instlayout)

        buttonListen01= QPushButton("Encouter premier son", self)
        layoutV.addWidget(buttonListen01)
        buttonListen01.setStyleSheet("background-color: white")
        buttonListen01.clicked.connect(self.Listen01Clicked)

        buttonListen02= QPushButton("Ecouter second son", self)
        layoutV.addWidget(buttonListen02)
        buttonListen02.setStyleSheet("background-color: white")
        buttonListen02.clicked.connect(self.Listen02Clicked)

        Hlayout02 = QHBoxLayout() #creer un calque "honrizontal"
        Hlayout02.addWidget(buttonListen01) # et ajoute lui un widget ici un bouton
        Hlayout02.addWidget(buttonListen02) # et ajoutes lui un  2 ème bouton



        layoutV.addLayout(Hlayout02)


        Boutongraph1 = QPushButton("Periodogramme 01",self) # creer un bouton à l'écran oK mais cela ne dit pas ou
        layoutV.addWidget(Boutongraph1) # ce bouton met le dans le calque layoutV maintenant je sais ou est le bouton
        Boutongraph1.clicked.connect(self.plotPeriodo01)
        Boutongraph2 = QPushButton("Periodogramme 02",self)
        layoutV.addWidget(Boutongraph2)
        Boutongraph2.clicked.connect(self.plotPeriodo02)

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




    def plotPeriodo01(self,canvas3):
        Fichier01 = "File01"
        data = affiche_perido(Fichier01)
        self._static_ax.plot(data)
        self._static_ax.figure.canvas.draw()

    def plotPeriodo02(self,canvas3):
        Fichier02 = "File02"
        data = affiche_perido(Fichier02)
        self._dynamic_ax.plot(data)
        self._dynamic_ax.figure.canvas.draw()




    def Record01Clicked(self) :

        print("Record1")
        enregistrer_static("File01",3)

    def Record02Clicked(self) :
        print("Record1")
        enregistrer_static("File02",3)

    def Listen01Clicked(self) :
        pass
    def Listen02Clicked(self) :
        pass




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
        self.setWindowTitle("Physique du Son")
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
        Boutongraph1 = QPushButton("Periodogramme",self) # creer un bouton à l'écran oK mais cela ne dit pas ou
        layoutV.addWidget(Boutongraph1) # ce bouton met le dans le calque layoutV maintenant je sais ou est le bouton
        Boutongraph1.clicked.connect(self.plotPeriodo)
        Boutongraph2 = QPushButton("Courbe",self)
        layoutV.addWidget(Boutongraph2)
        Boutongraph2.clicked.connect(self.sinusoiddynamyque)

        Hlayout = QHBoxLayout() #creer un calque "honrizontal"
        Hlayout.addWidget(Boutongraph1) # et ajoute lui un widget ici un bouton
        Hlayout.addWidget(Boutongraph2) # et ajoutes lui un  2 ème bouton

        layoutV.addLayout(Hlayout)  # et ajoute le Hlayout dans le Layout vertical

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))  # creer un canevas
        layoutV.addWidget(static_canvas) # et mets le dans le layoutV

        ToolBar1= NavigationToolbar(static_canvas, self)

        self.addToolBar(ToolBar1) # ajoutes lui aussi une barre de navigation

        layoutV.addWidget(ToolBar1)  # et met la NavigationToolbar sur le layout qui va bien
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
        #print(img)
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

    def plotPeriodo(self,canvas3):
        data = affiche_perido()
        self._static_ax.plot(data)
        self._static_ax.figure.canvas.draw()

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

    def RecordClicked(self) :
        dialog = RecordWindow(self)
        self.dialogs.append(dialog)
        dialog.show()

    def OndeClicked(self) :
        dialog = Ondewindow(self)
        self.dialogs.append(dialog)
        dialog.show()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)



        self.dialogs = list()

        buttonWarmUp= QPushButton("Je chauffe", self)
        buttonWarmUp.move(270,500)
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

        buttonRecord= QPushButton("Je m'enregistre", self)
        buttonRecord.move(580,500)
        buttonRecord.setFixedHeight(50)
        buttonRecord.setFixedWidth(125)
        buttonRecord.setStyleSheet("background-color: white")
        buttonRecord.clicked.connect(self.RecordClicked)


        buttonPhysic= QPushButton("Physique du son", self)
        buttonPhysic.move(1000,500)
        buttonPhysic.setFixedHeight(50)
        buttonPhysic.setFixedWidth(125)
        buttonPhysic.setStyleSheet("background-color: white")
        buttonPhysic.clicked.connect(self.PhysicClicked)

        buttonOnde= QPushButton("Forme d'onde", self)
        buttonOnde.move(500,600)
        buttonOnde.setFixedHeight(50)
        buttonOnde.setFixedWidth(125)
        buttonOnde.setStyleSheet("background-color: white")
        buttonOnde.clicked.connect(self.OndeClicked)








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


