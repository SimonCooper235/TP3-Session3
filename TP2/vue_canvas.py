from PyQt6.QtWidgets import QMessageBox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_template import FigureCanvas


from modele_liste_fonctions import ModeleListeFonctions


class MPLCanvas(FigureCanvas):
    __model : ModeleListeFonctions

    def __init__(self, model : ModeleListeFonctions):

        self.__fig, self.__ax = plt.subplots()

        super().__init__()

        self.__model = model
        self.__model.modelChanged.connect(self.dessiner)

    def dessiner(self):
        try :
            self.__ax.clear()
            f = self.__model.fonction
            if f :
                x = np.linspace(self.__model.borneInf, self.__model.borneSup, 1000)
                y= f(x)
                self.__ax.plot(x, y)
            self.draw()
        except Exception as e :
            QMessageBox.critical(self, "Erreur", "la fonction est invalide")