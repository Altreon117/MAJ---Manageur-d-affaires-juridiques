import os
from PyQt6.QtWidgets import QFrame, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QIcon

from config import APP_NAME, ICON_PATH, WINDOW_WIDTH, WINDOW_HEIGHT
from config import THEME_LIGHT, THEME_DARK, get_stylesheet

#Pour Windows, pour que l'icône de l'application apparaisse dans la barre des tâches
if os.name == 'nt':
    import ctypes
    myappid = 'drgoetz.gestioncabinet.app.1' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Propriétés de la fenêtre (contrôlées par config.py)
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(get_stylesheet(THEME_LIGHT))
        
        #Création du widget central (obligatoire dans un QMainWindow)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        #Application d'un layout au widget central
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # --- LE HEADER ---
        self.header_frame = QFrame()
        self.header_frame.setObjectName("header_frame")
        self.header_frame.setFixedHeight(70)
        
        # --- LE BODY (Corps de la page) ---
        self.body_widget = QWidget()
        self.body_layout = QVBoxLayout(self.body_widget)
        self.body_layout.setContentsMargins(20, 20, 20, 20)
        
        #Assemblage final
        self.main_layout.addWidget(self.header_frame)
        self.main_layout.addWidget(self.body_widget)