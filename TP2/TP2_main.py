import sys

from PyQt6.QtWidgets import QApplication

from vue_principale import VuePrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = VuePrincipal()
    fenetre.show()
    sys.exit(app.exec())