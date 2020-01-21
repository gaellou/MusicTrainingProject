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

Diapason = 440
FréquenceLaInstrument = Diapason
Tempo = 85

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ApplicationWindow, self).__init__()

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layoutV = QtWidgets.QVBoxLayout(self._main)
        self.setWindowTitle("test")
        self.setGeometry(20, 20, 1000, 1000)

        self.statusBar().showMessage('Ready')  # Faire une barre de status



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
        NomFichier = './IMAGE/Exercices/Ex11.png'
        img = mpimg.imread(NomFichier)
        print(img)
        imgplot = plt.imshow(img)
        self._static_ax .imshow(img)
        self._static_ax.set_title('PyQt Matplotlib Example')
        self._static_ax .figure.canvas.draw()

class MainWindow(QtWidgets.QMainWindow):

    def WarmUpClicked(self) :
        dialog = ApplicationWindow(self)
        self.dialogs.append(dialog)
        dialog.show()


    def PracticeClicked(self) :
        pass



    def SolfegeClicked(self) :
        pass


    def PhysicClicked(self) :
        pass

    def ChangeDiapason(self, CheckBox, Diapason) :
        pass



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)


        self.CheckTrp = self.findChild(QtWidgets.QPushButton, 'CheckTrumpet')
        self.CheckFl = self.findChild(QtWidgets.QPushButton, 'CheckFlute')
        self.CheckCl = self.findChild(QtWidgets.QPushButton, 'CheckClarinet')
        self.CheckVl = self.findChild(QtWidgets.QPushButton, 'CheckViolin')


        buttonWarmUp= QPushButton("Je chauffe", self)
        buttonWarmUp.move(90,500)
        buttonWarmUp.setFixedHeight(50)
        buttonWarmUp.setStyleSheet("background-color: white")
        buttonWarmUp.clicked.connect(self.WarmUpClicked)

        self.dialogs = list()

        buttonPractice= QPushButton("Je m'entraine", self)
        buttonPractice.move(430,500)
        buttonPractice.setFixedHeight(50)
        buttonPractice.setStyleSheet("background-color: white")
        buttonPractice.clicked.connect(self.PracticeClicked)

        buttonSolfege= QPushButton("Solfège", self)
        buttonSolfege.move(790,500)
        buttonSolfege.setFixedHeight(50)
        buttonSolfege.setStyleSheet("background-color: white")
        buttonSolfege.clicked.connect(self.SolfegeClicked)


        buttonPhysic= QPushButton("Physique du son", self)
        buttonPhysic.move(1200,500)
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


