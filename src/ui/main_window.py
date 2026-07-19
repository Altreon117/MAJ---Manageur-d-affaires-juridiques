import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QIcon

from config import APP_NAME, ICON_PATH, WINDOW_WIDTH, WINDOW_HEIGHT

#Pour Windows, pour que l'icône de l'application apparaisse dans la barre des tâches
if os.name == 'nt':
    import ctypes
    myappid = 'drgoetz.gestioncabinet.app.1' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Propriétés de la fenêtre (contrôlées par config.py)
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # 2. Création du widget central (obligatoire dans un QMainWindow)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 3. Application d'un layout au widget central
        layout = QVBoxLayout(central_widget)