import sys
import time
import random
import numpy as np

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



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
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


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
