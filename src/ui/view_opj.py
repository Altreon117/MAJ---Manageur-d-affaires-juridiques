from PyQt6.QtWidgets import QFrame, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt

from src.backend.excel_manager import ExcelManager
from src.ui.card_opj_component import CardOPJComponent

class OPJView(QWidget):
    def __init__(self):
        super().__init__()
        
        # LAYOUT PRINCIPAL DE LA PAGE
        # On utilise QHBoxLayout pour séparer la Gauche (Filtres) et la Droite (Contenu)
        main_layout = QHBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- PARTIE GAUCHE - FILTRE ---
        self.filter_frame = QFrame()
        self.filter_frame.setObjectName("filter_frame")
        
        filter_layout = QVBoxLayout(self.filter_frame)
        filter_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_filtre = QLabel("FILTRE")
        lbl_filtre.setStyleSheet("font-size: 20px; font-weight: bold;")
        filter_layout.addWidget(lbl_filtre)
        filter_layout.addStretch()
        
        # --- PARTIE DROITE - GRAND BODY ---
        self.grand_body_frame = QFrame()
        self.grand_body_frame.setObjectName("grand_body_frame")
        
        grand_body_layout = QVBoxLayout(self.grand_body_frame)
        grand_body_layout.setContentsMargins(0, 0, 0, 0)
        grand_body_layout.setSpacing(20)
        
        # --- PARTIE DROITE HAUTE - RECHERCHE / TRI ---
        self.tri_frame = QFrame()
        self.tri_frame.setObjectName("tri_frame")
        tri_layout = QVBoxLayout(self.tri_frame)
        tri_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_recherche = QLabel("RECHERCHER :")
        lbl_tri = QLabel("TRIER PAR :")
        lbl_recherche.setStyleSheet("font-size: 16px;")
        lbl_tri.setStyleSheet("font-size: 16px;")
        
        tri_layout.addWidget(lbl_recherche)
        tri_layout.addWidget(lbl_tri)
        
        # --- PARTIE DROITE BASSE - LITTLE BODY ---
        # 1. On crée la zone de défilement
        self.little_body_scroll_area = QScrollArea()
        self.little_body_scroll_area.setWidgetResizable(True)
        self.little_body_scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        # 2. On crée un widget "conteneur" qui ira à l'intérieur du ScrollArea
        self.list_container = QWidget()
        self.list_container.setObjectName("list_container")
        self.list_container.setStyleSheet("#list_container { background-color: transparent; }")
        
        # 3. On lui donne un Layout vertical pour empiler les cartes
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10) # Espace de 10px entre chaque carte
        
        # 4. On appelle notre fonction d'injection des données
        self.charger_donnees_excel()
        
        # 5. On place le conteneur rempli de cartes dans la zone de défilement
        self.little_body_scroll_area.setWidget(self.list_container)
        
        # --- ASSEMBLAGE DE LA PARTIE DROITE ---
        grand_body_layout.addWidget(self.tri_frame, 1)
        grand_body_layout.addWidget(self.little_body_scroll_area, 4)
        
        # --- ASSEMBLAGE FINAL DE LA PAGE ---
        main_layout.addWidget(self.filter_frame, 1) 
        main_layout.addWidget(self.grand_body_frame, 4)
        
    def charger_donnees_excel(self):
        """Lit l'Excel et peuple la vue avec les composants CardOPJComponent."""
        # On demande au backend de lire l'onglet "OPJ"
        lignes_excel = ExcelManager.read_sheet("OPJ")
        
        if not lignes_excel:
            lbl_vide = QLabel("Aucun dossier trouvé dans l'onglet OPJ.")
            lbl_vide.setStyleSheet("color: gray; font-style: italic;")
            self.list_layout.addWidget(lbl_vide)
            return
            
        # Pour chaque ligne trouvée, on crée une carte et on l'ajoute au layout
        for row in lignes_excel:
            carte = CardOPJComponent(row)
            self.list_layout.addWidget(carte)