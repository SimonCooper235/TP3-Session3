from PyQt6.QtWidgets import QMainWindow, QLineEdit, QVBoxLayout, QMessageBox
from PyQt6.uic import loadUi


from modele_liste_fonctions import ModeleListeFonctions
from vue_canvas import MPLCanvas


class VuePrincipal(QMainWindow):
    fonctionLineEdit : QLineEdit()
    borneInfLineEdit : QLineEdit()
    borneSupLineEdit : QLineEdit()
    matplotlibVLayout : QVBoxLayout()

    __model = ModeleListeFonctions
    def __init__(self):
        super().__init__()
        loadUi('ui/fenêtre_principale.ui', self)

        self.model = ModeleListeFonctions()
        canvas = MPLCanvas(self.model)

        self.matplotlibVLayout.insertWidget(0, canvas)

        self.fonctionLineEdit.editingFinished.connect(self.on_fonction_edited)
        self.borneInfLineEdit.text_changed.connect(self.on_borne_edited(self.borneInfLineEdit))
        self.borneSupLineEdit.text_changed.connect(self.on_borne_edited(self.borneSupLineEdit))





    def on_fonction_edited(self):
        #Attention la validation n'est pas implémentée dans ce corrigé, c'est voulu...
        fonct_str = self.fonctionLineEdit.text()
        if self.model.validate_fonction(fonct_str) :
            self.model.fonction = fonct_str
        else :
            QMessageBox.critical(self, "Erreur", "La fonction est invalide")
            self.fonctionLineEdit.clear()
            self.fonctionLineEdit.setStyleSheet("background-color: red;")

    def on_borne_edited(self, borne):
        borne_str = borne.text()
        if self.model.validate_bornes(borne_str):
            if borne_str is self.borneInfLineEdit.text():
                self.model.borneInf(borne_str)
            elif borne_str is self.borneSupLineEdit.text():
                self.model.borneSup(borne_str)
        else:
            if borne_str is self.borneInfLineEdit.text():
                self.borneInfLineEdit.setStyleShee("background-color : red;")
            elif borne_str is self.borneSupLineEdit.text():
                self.borneSupLineEdit.setStyleShee("background-color : red;")