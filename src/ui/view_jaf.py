from PyQt6.QtWidgets import QFrame, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QScrollArea, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

from config import JAF_BACK_COLUMNS, JAF_FRONT_COLUMNS
from src.backend.excel_manager import ExcelManager
from src.ui.card_jaf_component import CardJAFComponent

class JAFView(QWidget):
    def __init__(self):
        super().__init__()
        
        self.active_sort_button = None
        self.current_sort_column = None
        
        self.all_cards = []
        
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
        
        # --- Ligne 2 : TRI (Génération dynamique des boutons switch) ---
        tri_row_layout = QHBoxLayout()
        tri_row_layout.setSpacing(10)
        
        lbl_tri = QLabel("TRIER PAR :")
        lbl_tri.setStyleSheet("font-size: 16px; font-weight: bold;")
        tri_row_layout.addWidget(lbl_tri)
        
        # Pour chaque colonne back, on crée un bouton switch cliquable
        for col_name in JAF_BACK_COLUMNS:
            btn = QPushButton(col_name)
            btn.setObjectName("sort_button")
            btn.setCheckable(True) # 💡 Rend le bouton "basculable" (toggle)
        
            # On connecte le clic en passant le nom de la colonne et le bouton lui-même
            btn.clicked.connect(lambda checked, c=col_name, b=btn: self.gerer_tri(c, b))
        
            tri_row_layout.addWidget(btn)
        
        tri_row_layout.addStretch()
        
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
            
            self.all_cards.append(carte)
            
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
                
    def appliquer_tri(self, nom_colonne=None):
            """Trie visuellement les cartes dans le layout."""
            # 1. On retire toutes les cartes du layout (sans les détruire de la mémoire)
            while self.list_layout.count():
                item = self.list_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None) # Détache visuellement le widget
    
            # 2. On détermine la liste triée
            if nom_colonne is None:
                # Si aucun tri n'est demandé, on reprend la liste dans l'ordre d'origine
                cartes_triees = self.all_cards
            else:
                # 💡 MAGIE PYTHON : On trie la liste en regardant dans le dictionnaire row_data de chaque carte
                cartes_triees = sorted(
                    self.all_cards, 
                    # On met tout en minuscules (lower) pour qu'un "a" et un "A" soient classés ensemble
                    key=lambda carte: str(carte.row_data.get(nom_colonne, "")).lower()
                )
    
            # 3. On réinjecte les cartes dans le layout dans le bon ordre
            for carte in cartes_triees:
                self.list_layout.addWidget(carte)
    
    def gerer_tri(self, nom_colonne, clicked_button):
        """Gère la logique exclusive des boutons de tri (Switch & Toggle)."""
        if self.active_sort_button == clicked_button:
            # Cas 1 : Désactivation du tri
            clicked_button.setChecked(False)
            self.active_sort_button = None
            self.current_sort_column = None
            
            # 💡 On annule le tri (retour à l'ordre d'origine)
            self.appliquer_tri(None)
            
        else:
            # Cas 2 : Un autre bouton était actif, on l'éteint
            if self.active_sort_button is not None:
                self.active_sort_button.setChecked(False)
            
            # Cas 3 : Activation du nouveau tri
            self.active_sort_button = clicked_button
            self.current_sort_column = nom_colonne
            clicked_button.setChecked(True)
            
            # 💡 On lance le tri sur la colonne demandée
            self.appliquer_tri(nom_colonne)