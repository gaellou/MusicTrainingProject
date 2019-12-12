import sys
import time
import random
import numpy as np
 
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
 
        mainMenu = self.menuBar()  #creer d'abord une barre de menu vide avant de la remplir d'entête de menus divers
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu('Fichier')  # tapes l'entête du menu
        helpMenu = mainMenu.addMenu('Aide')
        EditMenu = mainMenu.addMenu('Editer')
        OuvrirFichier = QAction(QIcon('Fichier.png'),'Ouvrir',self)
        OuvrirFichier.setShortcut('Ctrl+O')
        OuvrirFichier.setStatusTip('Ouvrir un fichier')
        OuvrirFichier.triggered.connect(self.repaint)
        fileMenu.addAction(OuvrirFichier) # Cette une des ligne du menu tape le menu 'Ouvrir un fichier à l'écran 
        exitMenu = QAction(QIcon('exit24.png'), 'Exit', self)
        exitMenu.setShortcut('Ctrl+Q')
        exitMenu.setStatusTip('Exit application')
        exitMenu.triggered.connect(self.close)  # ferme l'application en prenant le menu Fichier
        fileMenu.addAction(exitMenu)
 
        Boutongraph1 = QPushButton("Drole de graphe",self) # creer un bouton à l'écran oK mais cela ne dit pas ou 
        layoutV.addWidget(Boutongraph1) # ce bouton met le dans le calque layoutV maintenant je sais ou est le bouton
        Boutongraph1.clicked.connect(self.graphstatic)
        Boutongraph2 = QPushButton("Courbe sinus",self)
        layoutV.addWidget(Boutongraph2)
        Boutongraph2.clicked.connect(self.sinusoiddynamyque)
        Boutongraph3 = QPushButton("Données aléatoires",self)
        layoutV.addWidget(Boutongraph3)
        Boutongraph3.clicked.connect(self.plotaleatoire)
 
        Hlayout = QHBoxLayout() #creer un calque "honrizontal"
        Hlayout.addWidget(Boutongraph1) # et ajoute lui un widget ici un bouton
        Hlayout.addWidget(Boutongraph2) # et ajoutes lui un  2 ème bouton
        Hlayout.addWidget(Boutongraph3) # et ajoute lui encore un bouton
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
        canvas3 = FigureCanvas(Figure(figsize=(5, 3)))  # creer un 3 ème canevas
        layoutV.addWidget(canvas3) # et met le aussi dans le layoutV
        ToolBar3 = NavigationToolbar(canvas3, self)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,ToolBar3)
        layoutV.addWidget(ToolBar3)  #et met la NavigationToolbar sur le layout qui va bien
 
        self._static_ax = static_canvas.figure.add_subplot(111)  # cette ligne ne pouvais pas être mis dans la fonction graphstatic sinon le bouton n'afficher pas le graphique  ce sont les axes du premier canevas appeler static_canvas
 
        self.axescanvas3 = canvas3.figure.add_subplot(111) # creer les axes du 3 ème canevas
 
        self._dynamic_ax = dynamic_canvas.figure.add_subplot(111) # creer les axes du 2 ème canevas le canevas dynamique
        #self._timer = dynamic_canvas.new_timer(100, [(self._update_canvas, (), {})])
        #self._timer.start()   # fonctionne mais sans le déclenchement du bouton
 
 
    def graphstatic(self,static_canvas):  # il fallait aussi transmettre le 2 ème paramètre static_canvas à la fonction graphstatic
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")
        self._static_ax.figure.canvas.draw()
 
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
 
    def plotaleatoire(self,canvas3):
 
        data = [random.random() for i in range(250)]
        #ax = self.figure.add_subplot(111)
        self.axescanvas3.plot(data, 'r-', linewidth = 0.5)
        self.axescanvas3.set_title('PyQt Matplotlib Example')
        self.axescanvas3.figure.canvas.draw()
 
 
if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()