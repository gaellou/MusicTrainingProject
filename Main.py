import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QDialog
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget, QPushButton
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

Diapason = 440
FréquenceLaInstrument = Diapason
Tempo = 85


class MainWindow(QtWidgets.QMainWindow):

    def WarmUpClicked(self) :
        pass


    def PracticeClicked(self) :
        pass



    def SolfegeClicked(self) :
        pass


    def PhysicClicked(self) :
        pass

    def ChangeDiapason(self, CheckBox, Diapason) :
        if (ChecBob.text="Trompette") :
            #rapport



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


