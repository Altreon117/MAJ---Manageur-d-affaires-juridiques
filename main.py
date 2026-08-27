import sys
import os

# Si l'app est compilée (frozen), Windows lira l'icône du .exe tout seul !
if os.name == 'nt' and not getattr(sys, 'frozen', False):
    import ctypes
    myappid = 'drgoetz.gestioncabinet.app.1' 
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception as e:
        pass
# -------------------------------------------------------------------------

# Maintenant que Windows est prévenu, on peut charger l'interface graphique
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from config import ICON_PATH
from src.ui.main_window import MainWindow

def main():
    # Création de l'application (le moteur PyQt6)
    app = QApplication(sys.argv)
    
    # On définit l'icône de l'application globalement
    app.setWindowIcon(QIcon(ICON_PATH))
    
    # Instanciation de notre fenêtre principale
    window = MainWindow()
    
    # Affichage de la fenêtre à l'écran
    window.show()
    
    # Lancement de la boucle d'événements
    sys.exit(app.exec())

if __name__ == "__main__":
    main()