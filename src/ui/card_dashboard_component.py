from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from config import STYLE_CARD_BODY

class CardDashboardComponent(QFrame):
    def __init__(self, titre_pin, valeur_pin="0"):
        super().__init__()
        
        self.setObjectName("card_dashboard")
        self.setMinimumSize(250, 150) # Pour avoir un beau rectangle
        
        # Layout principal de la carte (enlève les marges pour que le header touche les bords)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- PARTIE HAUTE (HEADER GRIS) ---
        self.header_frame = QFrame()
        self.header_frame.setObjectName("card_dashboard_header")
        self.header_frame.setFixedHeight(40)
        
        header_layout = QVBoxLayout(self.header_frame)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_titre = QLabel(titre_pin)
        self.lbl_titre.setObjectName("card_dashboard_title")
        header_layout.addWidget(self.lbl_titre)
        
        # --- PARTIE BASSE (CORPS BLANC AVEC VALEUR) ---
        self.body_frame = QFrame()
        self.body_frame.setStyleSheet(STYLE_CARD_BODY)
        
        body_layout = QVBoxLayout(self.body_frame)
        body_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_valeur = QLabel(str(valeur_pin))
        self.lbl_valeur.setObjectName("card_dashboard_value")
        body_layout.addWidget(self.lbl_valeur)
        
        # --- ASSEMBLAGE ---
        main_layout.addWidget(self.header_frame)
        main_layout.addWidget(self.body_frame)
        
    def mettre_a_jour_valeur(self, nouvelle_valeur):
        """Permet de changer le chiffre affiché sans recréer la carte."""
        self.lbl_valeur.setText(str(nouvelle_valeur))