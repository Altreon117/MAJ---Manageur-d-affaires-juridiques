from PyQt6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QScrollArea, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

from config import JAF_BACK_COLUMNS, JAF_FILTER_COLUMNS, JAF_FRONT_COLUMNS
from src.backend.excel_manager import ExcelManager
from src.ui.card_jaf_component import CardJAFComponent

class JAFView(QWidget):
    def __init__(self):
        super().__init__()
        
        self.active_sort_button = None
        self.current_sort_column = None
        
        self.all_cards = []
        
        self.filter_comboboxes = {}
        
        # LAYOUT PRINCIPAL DE LA PAGE
        main_layout = QHBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- PARTIE GAUCHE - FILTRE ---
        self.filter_frame = QFrame()
        self.filter_frame.setObjectName("filter_frame")
        self.filter_frame.setFixedWidth(250) # Pour respecter les proportions de ta maquette
        
        filter_layout = QVBoxLayout(self.filter_frame)
        filter_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Pousse tout vers le haut
        filter_layout.setContentsMargins(20, 20, 20, 20)
        filter_layout.setSpacing(15)
        
        lbl_filtre = QLabel("FILTRE")
        lbl_filtre.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        filter_layout.addWidget(lbl_filtre)
        
        # 💡 GÉNÉRATION DYNAMIQUE DES FILTRES DEPUIS LE DICTIONNAIRE
        for col_back, col_front in JAF_FILTER_COLUMNS.items():
            # Titre du filtre
            lbl = QLabel(col_front)
            lbl.setStyleSheet("font-size: 14px;")
        
            # Liste déroulante
            combo = QComboBox()
            combo.addItem("Sélectionner")
        
            # Connexion au moteur de filtre global à chaque changement
            combo.currentTextChanged.connect(self.appliquer_filtres_globaux)
        
            # Ajout au layout
            filter_layout.addWidget(lbl)
            filter_layout.addWidget(combo)
        
            # Sauvegarde dans notre dictionnaire (Clé = Nom Backend de la colonne)
            self.filter_comboboxes[col_back] = combo
        
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
        """Lit l'Excel et peuple la vue avec les composants."""
        lignes_excel = ExcelManager.read_sheet("OPJ", JAF_BACK_COLUMNS)
        self.all_cards.clear()
        
        if not lignes_excel:
            lbl_vide = QLabel("Aucun dossier trouvé dans l'onglet OPJ.")
            lbl_vide.setStyleSheet("color: gray; font-style: italic;")
            self.list_layout.addWidget(lbl_vide)
            return
            
        for row in lignes_excel:
            carte = CardJAFComponent(row, JAF_FRONT_COLUMNS)
            self.list_layout.addWidget(carte)
            self.all_cards.append(carte)
            
        # 💡 REMPLISSAGE DYNAMIQUE DES COMBOBOX (après avoir chargé les données)
        for col_back, combo in self.filter_comboboxes.items():
            # On utilise un set() pour éviter les doublons
            valeurs_uniques = set()
            for row in lignes_excel:
                val = str(row.get(col_back, "")).strip()
                if val: # Si la case n'est pas vide
                    valeurs_uniques.add(val)
            
            # On ajoute les valeurs triées par ordre alphabétique
            combo.addItems(sorted(list(valeurs_uniques)))
            
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
        """Trie visuellement les cartes dans le layout (vides à la fin, nombres respectés)."""
        # 1. On retire toutes les cartes du layout
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # 2. On détermine la liste triée
        if nom_colonne is None:
            # Annulation du tri : on remet l'ordre d'origine
            cartes_triees = self.all_cards
        else:
            # 💡 Fonction de tri sur-mesure (Type-Aware)
            def cle_de_tri(carte):
                valeur_brute = str(carte.row_data.get(nom_colonne, "")).strip()
                
                # Étape A : Est-ce que la case est vide ?
                est_vide = (valeur_brute == "")
                
                # Étape B : Est-ce un nombre ou du texte ?
                try:
                    # On tente de le convertir en chiffre décimal (float)
                    valeur_reelle = float(valeur_brute)
                    est_texte = False
                except ValueError:
                    # Si ça plante, c'est que c'est du vrai texte (ou un identifiant)
                    valeur_reelle = valeur_brute.lower()
                    est_texte = True
                    
                # Le tuple de tri final (Ordre de priorité) :
                # 1. `est_vide` : Les non-vides (False=0) s'affichent avant les vides (True=1)
                # 2. `est_texte`: Les nombres (False=0) s'affichent avant les textes purs (True=1)
                # 3. `valeur_reelle` : Tri mathématique naturel (500 < 1000) ou tri alphabétique (A < Z)
                return (est_vide, est_texte, valeur_reelle)

            # Application du tri avec notre nouvelle clé
            cartes_triees = sorted(self.all_cards, key=cle_de_tri)

        # 3. On réinjecte les cartes dans le bon ordre
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
            
    def appliquer_filtres_globaux(self, *args):
            """Croise la barre de recherche textuelle ET toutes les combobox."""
            texte_recherche = self.search_input.text().lower()
            
            # On parcourt la liste en mémoire, c'est beaucoup plus sûr et rapide
            for carte in self.all_cards:
                
                # 1. Validation de la barre de recherche
                match_texte = carte.correspond_a_la_recherche(texte_recherche)
                
                # 2. Validation des listes déroulantes
                match_combos = True
                for col_back, combo in self.filter_comboboxes.items():
                    valeur_choisie = combo.currentText()
                    
                    # Si l'utilisateur a sélectionné autre chose que le paramètre par défaut
                    if valeur_choisie != "Sélectionner":
                        # On vérifie ce que contient la carte pour cette colonne précise
                        valeur_carte = str(carte.row_data.get(col_back, "")).strip()
                        if valeur_carte != valeur_choisie:
                            match_combos = False
                            break # Inutile de tester les autres filtres, la carte est déjà éliminée
                
                # 3. Verdict final : La carte doit correspondre au texte ET aux combos
                carte.setVisible(match_texte and match_combos)