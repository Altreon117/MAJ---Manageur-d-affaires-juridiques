import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    #Création de l'application (le moteur PyQt6)
    app = QApplication(sys.argv)
    
    #Instanciation de notre fenêtre principale
    window = MainWindow()
    
    #Affichage de la fenêtre à l'écran
    window.show()
    
    #Lancement de la boucle d'événements (qui maintient l'app ouverte)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()