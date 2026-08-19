import os
from PyQt6.QtWidgets import QFrame, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QStackedWidget, QFileDialog
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt, QTimer, QSize

from config import APP_NAME, ICON_PATH, WINDOW_WIDTH, WINDOW_HEIGHT, MISE_A_JOUR_PAYEMENT_ICON_PATH
from config import THEME_LIGHT, THEME_DARK, get_stylesheet

from src.ui.view_dashboard import DashBoardView
from src.ui.view_opj import OPJView
from src.ui.view_jaf import JAFView
from src.ui.view_ji import JIView
from src.backend.excel_manager import ExcelManager

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
        
        # --- 1. LA BANNIÈRE DE NOTIFICATION (Cachée par défaut) ---
        self.notification_banner = QLabel(self)
        self.notification_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.notification_banner.hide()
        
       # --- 2. LE BOUTON FLOTTANT (FAB - Floating Action Button) ---
        self.fab_update = QPushButton(self.body_widget)
        self.fab_update.setObjectName("fab_update")
        self.fab_update.setFixedSize(70, 70) # Taille du cercle
        self.fab_update.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Ajout de l'icône rognée en cercle
        if os.path.exists(MISE_A_JOUR_PAYEMENT_ICON_PATH):
            # 1. On charge l'image originale
            original_pixmap = QPixmap(MISE_A_JOUR_PAYEMENT_ICON_PATH)
            
            # 2. On la redimensionne pour qu'elle remplisse au minimum 70x70
            scaled_pixmap = original_pixmap.scaled(
                70, 70, 
                Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                Qt.TransformationMode.SmoothTransformation
            )
            
            # 3. On crée un "calque" transparent de 70x70
            circular_pixmap = QPixmap(70, 70)
            circular_pixmap.fill(Qt.GlobalColor.transparent)
            
            # 4. On dessine l'image avec un masque circulaire (Antialiasing pour des bords lisses)
            painter = QPainter(circular_pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            path = QPainterPath()
            path.addEllipse(0, 0, 70, 70)
            painter.setClipPath(path)
            
            # Recentrage automatique de l'image
            x_offset = (70 - scaled_pixmap.width()) // 2
            y_offset = (70 - scaled_pixmap.height()) // 2
            painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
            painter.end()
            
            # 5. On applique l'image découpée comme icône à 100% de la taille du bouton
            self.fab_update.setIcon(QIcon(circular_pixmap))
            self.fab_update.setIconSize(QSize(70, 70))
            
            # On enlève le padding interne pour que l'image colle aux bords absolus
            self.fab_update.setStyleSheet("padding: 0px;")
            
        # Connexion au clic
        self.fab_update.clicked.connect(self.lancer_mise_a_jour)

    # --- 3. FONCTIONS DE MISE À JOUR ---
    
    def placer_bouton_flottant(self):
        """Calcule et applique la position du bouton en bas à droite."""
        x = self.body_widget.width() - 110 
        y = self.body_widget.height() - 110
        self.fab_update.move(x, y)
        self.fab_update.raise_() # Force le bouton à rester au premier plan

    def resizeEvent(self, event):
        """Événement déclenché à chaque fois que la fenêtre change de taille."""
        super().resizeEvent(event)
        self.placer_bouton_flottant()

    def showEvent(self, event):
        """Événement déclenché au tout premier affichage de la fenêtre."""
        super().showEvent(event)
        self.placer_bouton_flottant()

    def afficher_notification(self, message, is_error=False):
        """Affiche une bannière temporaire en haut de l'écran."""
        couleur = "#F44336" if is_error else "#4CAF50"
        style = f"background-color: {couleur}; color: white; font-weight: bold; padding: 15px; border-radius: 8px; font-size: 16px;"
        
        self.notification_banner.setStyleSheet(style)
        self.notification_banner.setText(message)
        self.notification_banner.adjustSize()
        
        # Centrage en haut
        x = (self.width() - self.notification_banner.width()) // 2
        self.notification_banner.move(x, 20)
        self.notification_banner.show()
        self.notification_banner.raise_() # Force à s'afficher par-dessus tout le reste
        
        # Disparition automatique après 4 secondes (4000 ms)
        QTimer.singleShot(4000, self.notification_banner.hide)

    def lancer_mise_a_jour(self):
        """Ouvre l'explorateur, lance le script et rafraîchit l'interface."""
        # Ouverture de l'explorateur de fichiers dans le dossier Télchargements par défaut
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner le fichier Excel de paiement", 
            "os.path.expanduser('~/Downloads')", 
            "Fichiers Excel (*.xlsx *.xls)"
        )
        
        if filepath:
            resultat = ExcelManager.update_payments(filepath)
            
            if resultat == -1:
                self.afficher_notification("Erreur : Impossible de lire la colonne 'Note'.", is_error=True)
            elif resultat == 0:
                self.afficher_notification("Aucun numéro correspondant trouvé dans les dossiers.", is_error=True)
            else:
                self.afficher_notification(f"Succès : {resultat} dossiers ont été mis à jour en 'payé' !")
                
                self.page_opj.charger_donnees_excel()
                self.page_jaf.charger_donnees_excel()
                self.page_ji.charger_donnees_excel()
                
                self.page_accueil.generer_cartes()