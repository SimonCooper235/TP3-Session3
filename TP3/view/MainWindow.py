import time
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QPushButton, QMainWindow, QVBoxLayout, QSpinBox, QProgressBar, QComboBox, QLineEdit
from PyQt6.uic import loadUi
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller.main_controller import MainController  # uniquement pour


class ProgressBar(QThread):
    progress = pyqtSignal()

    def __init__(self):
        super().__init__()
        if TYPE_CHECKING:
            self.__controller: MainController | None = None
            self.run()

    def run(self):
        time.sleep(5)

        self.progress.emit()

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

        self.progress_bar = ProgressBar()
        self.progress_bar.progress.connect(self.trouver_chemin)
        self.progress_bar.finished.connect(self.on_finished)
        self.progress_bar.start()

    def on_finished(self):
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.thread = None