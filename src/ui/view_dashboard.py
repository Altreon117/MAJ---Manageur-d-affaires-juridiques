from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

from config import DASHBOARD_AVAILABLE_PINS, DASHBOARD_DEFAULT_ACTIVE_PINS
from src.ui.card_dashboard_component import CardDashboardComponent
from src.backend.excel_manager import ExcelManager # 💡 Nouvel import du backend !

class DashBoardView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        # 💡 SUPPRESSION du AlignTop. Les "Stretch" plus bas vont centrer le tout automatiquement !
        
        self.cartes_affichees = []
        
        # --- CRÉATION DU TABLEAU ---
        self.board_ext_frame = QFrame()
        self.board_ext_frame.setObjectName("board_ext_frame")
        ext_layout = QVBoxLayout(self.board_ext_frame)
        ext_layout.setContentsMargins(20, 20, 20, 20)
        
        self.board_int_frame = QFrame()
        self.board_int_frame.setObjectName("board_int_frame")
        int_layout = QVBoxLayout(self.board_int_frame)
        int_layout.setContentsMargins(30, 30, 30, 30)
        int_layout.setSpacing(30)
        
        # --- LIGNE 1 : TITRE ET BOUTON ---
        header_layout = QHBoxLayout()
        
        titre = QLabel("DASHBOARD")
        titre.setStyleSheet("font-size: 32px; font-weight: bold;")
        
        self.btn_customize = QPushButton("Customize pins")
        self.btn_customize.setObjectName("sort_button") 
        self.btn_customize.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_customize.clicked.connect(self.ouvrir_fenetre_customisation)
        
        header_layout.addStretch() 
        header_layout.addWidget(titre)
        header_layout.addStretch() 
        header_layout.addWidget(self.btn_customize)
        
        # --- LIGNE 2 : LA GRILLE DE CARTES ---
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(40) 
        
        self.generer_cartes()
        
        # --- ASSEMBLAGE ET CENTRAGE VERTICAL ---
        int_layout.addLayout(header_layout)
        int_layout.addLayout(self.grid_layout)
        ext_layout.addWidget(self.board_int_frame)
        
        layout.addStretch() # 💡 Pousse le tableau vers le bas
        layout.addWidget(self.board_ext_frame)
        layout.addStretch() # 💡 Pousse le tableau vers le haut -> Centrage parfait !

    def generer_cartes(self):
        """Génère les 6 cartes dans la grille avec les vraies données."""
        for carte in self.cartes_affichees:
            carte.setParent(None)
        self.cartes_affichees.clear()
        
        # 💡 1. APPEL AU BACKEND POUR AVOIR LES VRAIS CHIFFRES
        metriques = ExcelManager.get_dashboard_metrics()
        
        for index, pin_key in enumerate(DASHBOARD_DEFAULT_ACTIVE_PINS):
            titre_propre = DASHBOARD_AVAILABLE_PINS.get(pin_key, "Inconnu")
            
            # 💡 2. RÉCUPÉRATION DE LA DONNÉE RÉELLE
            valeur_reelle = metriques.get(pin_key, 0)
            
            # Formatage spécial pour que les montants soient jolis (ex: "5 400 €")
            if pin_key == "montant_total":
                valeur_str = f"{valeur_reelle:,} €".replace(",", " ")
            else:
                valeur_str = str(valeur_reelle)
            
            carte = CardDashboardComponent(titre_propre, valeur_str)
            
            row = index // 3
            col = index % 3
            self.grid_layout.addWidget(carte, row, col)
            self.cartes_affichees.append(carte)

    def ouvrir_fenetre_customisation(self):
        """Sera appelée lors du clic sur 'Customize pins'."""
        print("Ouverture de la pop-up de customisation...")