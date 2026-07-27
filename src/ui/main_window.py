import os
from PyQt6.QtWidgets import QFrame, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QStackedWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

from config import APP_NAME, ICON_PATH, WINDOW_WIDTH, WINDOW_HEIGHT
from config import THEME_LIGHT, THEME_DARK, get_stylesheet

from src.ui.view_dashboard import DashBoardView
from src.ui.view_opj import OPJView
from src.ui.view_jaf import JAFView
from src.ui.view_ji import JIView

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
        self.header_frame.setFixedHeight(90)
        
        # Layout vertical interne du header
        header_layout = QVBoxLayout(self.header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        # --- PARTIE HAUTE (2/3) : Logo et Titre ---
        top_header_widget = QWidget()
        top_header_widget.setObjectName("top_header_widget")
        top_layout = QHBoxLayout(top_header_widget)
        top_layout.setContentsMargins(20, 0, 20, 0) # Marges gauche/droite pour ne pas coller au bord
        
        # Le Logo
        self.logo_label = QLabel()
        if os.path.exists(ICON_PATH):
            pixmap = QPixmap(ICON_PATH).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        
        # Le Titre
        self.title_label = QLabel(APP_NAME)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; border: none;")
        
        # Ajout au layout haut (aligné à gauche)
        top_layout.addWidget(self.logo_label)
        top_layout.addWidget(self.title_label)
        top_layout.addStretch() # Repousse tout le reste vers la gauche
        
        # --- PARTIE BASSE (1/3) : Les boutons de navigation ---
        bottom_header_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_header_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        
        # Création des 3 boutons
        self.btn_accueil = QPushButton("Accueil")
        self.btn_opj = QPushButton("OPJ")
        self.btn_jaf = QPushButton("JAF")
        self.btn_ji = QPushButton("JI")
        
        for btn in [self.btn_accueil, self.btn_opj, self.btn_jaf, self.btn_ji]:
            btn.setObjectName("nav_button")
            # QSizePolicy.Policy.Expanding force chaque bouton à prendre la place maximale disponible.
            # Comme il y en a 4, ils prendront exactement 1/4 chacun !
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            bottom_layout.addWidget(btn)
            
        # --- ASSEMBLAGE DU HEADER ---
        # Le 2 indique le facteur d'étirement (2 parts de hauteur)
        header_layout.addWidget(top_header_widget, 2) 
        # Le 1 indique le facteur d'étirement (1 part de hauteur)
        header_layout.addWidget(bottom_header_widget, 1)
        
        # --- LE BODY (Corps de la page) ---
        self.body_widget = QWidget()
        self.body_layout = QVBoxLayout(self.body_widget)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        
        #QStackedWidget
        self.stacked_widget = QStackedWidget()
        
        # INSTANCIATION DES PAGES (VUES)
        self.page_accueil = DashBoardView()
        self.page_opj = OPJView()
        self.page_jaf = JAFView()
        self.page_ji = JIView()
        # Ajout des pages au StackedWidget
        self.stacked_widget.addWidget(self.page_accueil) # Index 0
        self.stacked_widget.addWidget(self.page_opj)     # Index 1
        self.stacked_widget.addWidget(self.page_jaf)     # Index 2
        self.stacked_widget.addWidget(self.page_ji)      # Index 3

        # Ajout du StackedWidget dans le body
        self.body_layout.addWidget(self.stacked_widget)
        
        #Assemblage final
        self.main_layout.addWidget(self.header_frame)
        self.main_layout.addWidget(self.body_widget)
        
        # --- CONNEXION DES BOUTONS À LA NAVIGATION ---
        # On relie chaque bouton à une fonction lambda qui change l'index actif
        self.btn_accueil.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_opj.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_jaf.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_ji.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))