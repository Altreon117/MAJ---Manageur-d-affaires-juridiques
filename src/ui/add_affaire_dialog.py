from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QDialogButtonBox, QLabel, QComboBox, QWidget, QHBoxLayout)
from PyQt6.QtCore import Qt

from config import (STYLE_EDIT_DIALOG, STYLE_EDIT_BUTTONS, CHOIX_COLONNES, 
                    STYLE_EDIT_COMBOBOX, OPJ_FRONT_COLUMNS, JAF_FRONT_COLUMNS, JI_FRONT_COLUMNS)

class AddAffaireDialog(QDialog):
    def __init__(self, mission_sujet, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Créer une nouvelle affaire")
        self.resize(450, 550)
        self.setStyleSheet(STYLE_EDIT_DIALOG)

        self.inputs = {} # Stockera nos champs dynamiques
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # --- EN-TÊTE : Rappel du mail ---
        lbl_rappel = QLabel(f"<b>Issu du mail :</b> {mission_sujet}")
        lbl_rappel.setWordWrap(True)
        lbl_rappel.setStyleSheet("color: #555; background-color: #E0E0E0; padding: 10px; border-radius: 5px;")
        layout.addWidget(lbl_rappel)

        # --- SÉLECTEUR DE TYPE D'AFFAIRE ---
        type_layout = QHBoxLayout()
        lbl_type = QLabel("<b>Type de dossier :</b>")
        
        self.combo_type = QComboBox()
        self.combo_type.setStyleSheet(STYLE_EDIT_COMBOBOX)
        self.combo_type.addItems(["OPJ", "JAF", "JI"])
        # On connecte le changement à la regénération du formulaire
        self.combo_type.currentTextChanged.connect(self.generer_formulaire)
        
        type_layout.addWidget(lbl_type)
        type_layout.addWidget(self.combo_type)
        layout.addLayout(type_layout)

        # --- CONTENEUR DU FORMULAIRE DYNAMIQUE ---
        self.form_container = QWidget()
        self.form_layout = QFormLayout(self.form_container)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(15)
        layout.addWidget(self.form_container)

        # --- BOUTONS ---
        self.btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btn_box.setStyleSheet(STYLE_EDIT_BUTTONS)
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)
        
        layout.addStretch()
        layout.addWidget(self.btn_box)

        # On lance la première génération pour "OPJ" (sélectionné par défaut)
        self.generer_formulaire("OPJ")

    def generer_formulaire(self, type_affaire):
        """Détruit les anciens champs et regénère les nouveaux selon le type."""
        # 1. Nettoyage de l'ancien formulaire
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.inputs.clear()

        # 2. Sélection du bon dictionnaire
        colonnes_a_afficher = {}
        if type_affaire == "OPJ":
            colonnes_a_afficher = OPJ_FRONT_COLUMNS
        elif type_affaire == "JAF":
            colonnes_a_afficher = JAF_FRONT_COLUMNS
        elif type_affaire == "JI":
            colonnes_a_afficher = JI_FRONT_COLUMNS

        # 3. Création des champs
        for col_back, col_front in colonnes_a_afficher.items():
            if col_back in CHOIX_COLONNES:
                champ = QComboBox()
                champ.setStyleSheet(STYLE_EDIT_COMBOBOX)
                champ.addItems(CHOIX_COLONNES[col_back])
            else:
                champ = QLineEdit()
                champ.setPlaceholderText(f"Saisir {col_front.lower()}...")
                
            self.inputs[col_back] = champ
            self.form_layout.addRow(QLabel(col_front + " :"), champ)

    def get_data(self):
        """Récupère le type d'affaire ET les données typées."""
        new_data = {}
        for col_back, champ in self.inputs.items():
            if isinstance(champ, QComboBox):
                valeur_texte = champ.currentText().strip()
            else:
                valeur_texte = champ.text().strip()
                
            # Conversion numérique pour Pandas
            if valeur_texte.isdigit():
                valeur_finale = int(valeur_texte)
            else:
                try:
                    valeur_finale = float(valeur_texte)
                except ValueError:
                    valeur_finale = valeur_texte 
                    
            new_data[col_back] = valeur_finale
            
        return self.combo_type.currentText(), new_data