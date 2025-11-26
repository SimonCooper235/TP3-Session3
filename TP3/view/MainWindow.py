import time
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QPushButton, QMainWindow, QVBoxLayout, QSpinBox, QProgressBar, QComboBox, QLineEdit
from PyQt6.uic import loadUi
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller.main_controller import MainController  # uniquement pour


class CheminCourt(QThread):
    progress = pyqtSignal()

    def run(self):
        time.sleep(5)

        self.progress.emit()

class Sommets(QThread):
    sommets = pyqtSignal(int)

    def __init__(self, length):
        super().__init__()
        self.length = length


    def run(self):
        length = self.length
        for i in range(length):
            time.sleep(1)
            self.sommets.emit(i)

        time.sleep(1)

class MainWindow(QMainWindow):
    grapheLayout:QVBoxLayout

    createButton: QPushButton
    deleteButton: QPushButton
    nbrNodes:QSpinBox

    edgesComboBox:QComboBox
    weightSpinBox:QSpinBox
    deleteEdgeButton:QPushButton

    debutSpinbox: QSpinBox
    finSpinbox: QSpinBox
    progressBar: QProgressBar
    trouverCheminPushButton: QPushButton


    def __init__(self):
        super().__init__()
        loadUi("view/ui/main_window.ui", self)
        self.resize(1000,800)
        #self.draw_graphe()
        if TYPE_CHECKING:
            self.__controller: MainController | None = None

        self.trouverCheminPushButton.clicked.connect(self.lancer_thread)


    def add_canvas(self, canvas):
        #  insérer le canvas dans le layout
        self.grapheLayout.addWidget(canvas)

    def set_controller(self,controller):
        self.__controller = controller

    def trouver_chemin(self):
        debut = self.debutSpinBox.value()
        fin = self.finSpinBox.value()
        self.__controller.trouver_chemin(debut, fin)

    def lancer_thread(self):
        self.progressBar.setRange(0, 0)

        self.progress_bar = CheminCourt()
        self.progress_bar.progress.connect(self.trouver_chemin)
        self.progress_bar.finished.connect(self.on_finished)
        self.progress_bar.start()

    def on_finished(self):
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)

    def lancer_sommet(self):
        nombre_noeuds = self.nombre_noeuds()
        self.sommet = Sommets(nombre_noeuds)
        self.sommet.sommets.connect(self.mettre_a_jour)
        self.sommet.finished.connect(self.on_finished)
        self.sommet.start()

    def mettre_a_jour(self, valeur):
        nombre_noeuds = self.nombre_noeuds()
        self.progressBar.setValue(int(valeur / nombre_noeuds * 100))
        self.__controller.parcour_sommets(valeur)

    def on_finished(self):
        self.progressBar.setValue(0)

    def nombre_noeuds(self):
        return self.__controller.nombre_noeuds()

