from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('mainwindow.ui', self)

        self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])

    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()






    #bouton de la section de chauffe
            buttonWarmTrumpet= QPushButton("Trompette", self)
            buttonWarmTrumpet.move(100,400)
            buttonWarmTrumpet.setFixedHeight(50)
            buttonWarmTrumpet.setFixedWidth(125)
            buttonWarmTrumpet.setStyleSheet("background-color: white")
            buttonWarmTrumpet.hide()
            buttonWarmTrumpet.clicked.connect(self.WarmUpClicked)

            buttonWarmClarinet= QPushButton("Clarinette", self)
            buttonWarmClarinet.move(440,400)
            buttonWarmClarinet.setFixedHeight(50)
            buttonWarmClarinet.setFixedWidth(125)
            buttonWarmClarinet.setStyleSheet("background-color: white")
            buttonWarmClarinet.hide()
            buttonWarmClarinet.clicked.connect(self.WarmUpClicked)

            buttonWarmFlute= QPushButton("Flûte", self)
            buttonWarmFlute.move(800,400)
            buttonWarmFlute.setFixedHeight(50)
            buttonWarmFlute.setFixedWidth(125)
            buttonWarmFlute.setStyleSheet("background-color: white")
            buttonWarmFlute.hide()
            buttonWarmFlute.clicked.connect(self.WarmUpClicked)

            buttonWarmViolin= QPushButton("Violon", self)
            buttonWarmViolin.move(1210,400)
            buttonWarmViolin.setFixedHeight(50)
            buttonWarmViolin.setFixedWidth(125)
            buttonWarmViolin.setStyleSheet("background-color: white")
            buttonWarmViolin.hide()
            buttonWarmUp.clicked.connect(self.WarmUpClicked)

            #bouton de la section entrainement

            buttonPracticeTrumpet= QPushButton("Trompette", self)
            buttonPracticeTrumpet.move(100,400)
            buttonPracticeTrumpet.setFixedHeight(50)
            buttonPracticeTrumpet.setFixedWidth(125)
            buttonPracticeTrumpet.setStyleSheet("background-color: white")
            buttonPracticeTrumpet.hide()

            buttonPracticeClarinet= QPushButton("Clarinette", self)
            buttonPracticeClarinet.move(440,400)
            buttonPracticeClarinet.setFixedHeight(50)
            buttonPracticeClarinet.setFixedWidth(125)
            buttonPracticeClarinet.setStyleSheet("background-color: white")
            buttonPracticeClarinet.hide()

            buttonPracticeFlute= QPushButton("Flûte", self)
            buttonPracticeFlute.move(800,400)
            buttonPracticeFlute.setFixedHeight(50)
            buttonPracticeFlute.setFixedWidth(125)
            buttonPracticeFlute.setStyleSheet("background-color: white")
            buttonPracticeFlute.hide()

            buttonPracticeViolin= QPushButton("Violon", self)
            buttonPracticeViolin.move(1210,400)
            buttonPracticeViolin.setFixedHeight(50)
            buttonPracticeViolin.setFixedWidth(125)
            buttonPracticeViolin.setStyleSheet("background-color: white")
            buttonPracticeViolin.hide()
