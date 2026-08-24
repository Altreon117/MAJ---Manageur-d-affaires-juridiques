from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

from config import STYLE_DASHBOARD_TITLE

from config import DASHBOARD_AVAILABLE_PINS, DASHBOARD_DEFAULT_ACTIVE_PINS
from src.ui.card_dashboard_component import CardDashboardComponent
from src.backend.excel_manager import ExcelManager
from src.ui.customize_pins_dialog import CustomizePinsDialog

class DashBoardView(QWidget):
    def __init__(self):
        super().__init__()
        
        self.active_pins = DASHBOARD_DEFAULT_ACTIVE_PINS.copy()
        
        layout = QVBoxLayout(self)
        
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
        titre.setStyleSheet(STYLE_DASHBOARD_TITLE)
        
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
        
        layout.addStretch()
        layout.addWidget(self.board_ext_frame)
        layout.addStretch()

    def generer_cartes(self):
        """Génère les 6 cartes dans la grille avec les vraies données."""
        for carte in self.cartes_affichees:
            carte.setParent(None)
        self.cartes_affichees.clear()
        
        metriques = ExcelManager.get_dashboard_metrics()
        
        for index, pin_key in enumerate(self.active_pins):
            titre_propre = DASHBOARD_AVAILABLE_PINS.get(pin_key, "Inconnu")
            valeur_reelle = metriques.get(pin_key, 0)
            
            # Formatage spécial
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
        dialog = CustomizePinsDialog(self.active_pins, self)
        
        # Si l'utilisateur clique sur "Save" et que la validation passe
        if dialog.exec():
            # On récupère la nouvelle sélection
            nouvelle_selection = dialog.get_selected_pins()
            self.active_pins = nouvelle_selection
            
            # On regénère les cartes instantanément !
            self.generer_cartes()