from PyQt6.QtWidgets import QFrame, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QScrollArea, QLineEdit
from PyQt6.QtCore import Qt

from config import JAF_BACK_COLUMNS, JAF_FRONT_COLUMNS
from src.backend.excel_manager import ExcelManager
from src.ui.card_jaf_component import CardJAFComponent

class JAFView(QWidget):
    def __init__(self):
        super().__init__()
        
        # LAYOUT PRINCIPAL DE LA PAGE
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
        
        # Layout vertical principal pour cette zone (pour empiler Recherche puis Tri)
        tri_layout = QVBoxLayout(self.tri_frame)
        # On ajoute des marges internes pour que ça respire un peu
        tri_layout.setContentsMargins(15, 15, 15, 15) 
        tri_layout.setSpacing(15) # Espace entre la ligne de recherche et la ligne de tri
        
        # --- Ligne 1 : RECHERCHE (Horizontal) ---
        recherche_layout = QHBoxLayout()
        
        lbl_recherche = QLabel("RECHERCHER :")
        lbl_recherche.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        # Création de la barre de saisie
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Saisissez un nom, une référence...")
        self.search_input.setFixedHeight(35)
        # Style de la barre de recherche (bordure neutre par défaut, mauve au focus)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #A4ACAFFF;
                border-radius: 5px;
                padding-left: 10px;
                font-size: 14px;
                background-color: #FFFFFF;
            }
            QLineEdit:focus {
                border: 2px solid #bca0dc;
            }
        """)
        
        self.search_input.textChanged.connect(self.filtrer_en_temps_reel)
        
        recherche_layout.addWidget(lbl_recherche)
        recherche_layout.addWidget(self.search_input)
        
        # --- Ligne 2 : TRI (Horizontal) ---
        tri_row_layout = QHBoxLayout()
        
        lbl_tri = QLabel("TRIER PAR :")
        lbl_tri.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        tri_row_layout.addWidget(lbl_tri)
        tri_row_layout.addStretch() # Pousse le label à gauche, laisse la place pour les futurs boutons
        
        # --- Assemblage des lignes dans le cadre ---
        tri_layout.addLayout(recherche_layout)
        tri_layout.addLayout(tri_row_layout)
        
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
        """Lit l'Excel et peuple la vue avec les composants CardJAFComponent."""
        # On demande au backend de lire l'onglet "JAF"
        lignes_excel = ExcelManager.read_sheet("JAF", JAF_BACK_COLUMNS)
        
        if not lignes_excel:
            lbl_vide = QLabel("Aucun dossier trouvé dans l'onglet JAF.")
            lbl_vide.setStyleSheet("color: gray; font-style: italic;")
            self.list_layout.addWidget(lbl_vide)
            return
            
        # Pour chaque ligne trouvée, on crée une carte et on l'ajoute au layout
        for row in lignes_excel:
            carte = CardJAFComponent(row, JAF_FRONT_COLUMNS)
            self.list_layout.addWidget(carte)
            
    def filtrer_en_temps_reel(self, texte_recherche):
        """Parcourt le layout et masque les cartes qui ne correspondent pas au texte."""
        
        # On boucle sur tous les éléments présents dans la zone de défilement
        for i in range(self.list_layout.count()):
            item = self.list_layout.itemAt(i)
            widget = item.widget()
            
            # Sécurité : on vérifie que le widget existe et que c'est bien une "Carte" 
            # (en vérifiant s'il possède la méthode qu'on vient de créer)
            if widget and hasattr(widget, "correspond_a_la_recherche"):
                # On demande à la carte si elle correspond. 
                # Si oui (True), elle s'affiche. Si non (False), elle se masque instantanément.
                correspond = widget.correspond_a_la_recherche(texte_recherche)
                widget.setVisible(correspond)