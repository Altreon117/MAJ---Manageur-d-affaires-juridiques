from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QSizePolicy, QHBoxLayout, QPushButton, QWidget
from PyQt6.QtCore import Qt

from src.ui.edit_affaire_dialog import EditAffaireDialog
from src.backend.excel_manager import ExcelManager
from config import STYLE_CARD_EDIT_BUTTON

class CardJIComponent(QFrame):
    def __init__(self, row_data, colonnes_a_afficher, callback_maj=None):
        super().__init__()
        
        self.row_data = row_data 
        self.colonnes_a_afficher = colonnes_a_afficher 
        self.callback_maj = callback_maj
        
        self.setObjectName("card_ji")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # --- LAYOUT GLOBAL (Horizontal pour séparer les infos du bouton) ---
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)
        
        # 1. Zone des informations textuelles
        info_widget = QWidget()
        info_widget.setStyleSheet("background-color: transparent;")
        grid_layout = QGridLayout(info_widget)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setHorizontalSpacing(50) 
        grid_layout.setVerticalSpacing(10)   
        
        for index, (col_back, col_front) in enumerate(colonnes_a_afficher.items()):
            valeur = str(row_data.get(col_back, "N/A")).strip()
            if valeur.endswith(".0"):
                valeur = valeur[:-2]
                
            # Nettoyage spécifique des dates Pandas
            if " 00:00:00" in valeur:
                valeur = valeur.replace(" 00:00:00", "")
                if "-" in valeur and len(valeur) == 10:
                    annee, mois, jour = valeur.split("-")
                    valeur = f"{jour}/{mois}/{annee}"
                    
            lbl = QLabel(f"<b>{col_front}</b> : {valeur}")
            if col_back == "NOM":
                lbl.setObjectName("card_label_nom")
            else:
                lbl.setObjectName("card_label_normal")
        
            row = index // 2
            col = index % 2
            grid_layout.addWidget(lbl, row, col)

        # 2. Bouton d'édition placé sur la droite
        self.btn_edit = QPushButton("Modifier")
        self.btn_edit.setFixedSize(80, 35)
        self.btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit.setStyleSheet(STYLE_CARD_EDIT_BUTTON)
        self.btn_edit.clicked.connect(self.ouvrir_edition)

        main_layout.addWidget(info_widget)
        main_layout.addWidget(self.btn_edit, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    def correspond_a_la_recherche(self, texte_recherche):
        if not texte_recherche:
            return True 
            
        texte_min = texte_recherche.lower()
        
        for valeur in self.row_data.values():
            if texte_min in str(valeur).lower():
                return True
                
        return False

    def ouvrir_edition(self):
        """Ouvre la popup d'édition, lance la sauvegarde, rafraîchit et notifie l'utilisateur."""
        dialog = EditAffaireDialog(self.row_data, self.colonnes_a_afficher, self)
        
        if dialog.exec(): 
            nouvelles_donnees = dialog.get_new_data()
            
            # 1. Demande au Backend d'appliquer les changements
            succes = ExcelManager.update_row("JI", self.row_data, nouvelles_donnees)
            
            # 2. Récupération de la fenêtre principale (MainWindow) pour utiliser ses fonctions
            fenetre_principale = self.window()
            nom_affaire = self.row_data.get("NOM", "L'affaire")
            
            if succes:
                # 3. On force la page à se recharger pour voir les modifications
                if self.callback_maj:
                    self.callback_maj()
                    
                # 4. On lance la belle notification verte en haut de l'écran !
                if hasattr(fenetre_principale, "afficher_notification"):
                    fenetre_principale.afficher_notification(f"Succès : Les données de {nom_affaire} ont été modifiées !")
            
            else:
                # 5. En cas de problème (fichier Excel ouvert ailleurs, etc.), on affiche une notification rouge
                if hasattr(fenetre_principale, "afficher_notification"):
                    fenetre_principale.afficher_notification(f"Erreur : Impossible de modifier {nom_affaire}.", is_error=True)