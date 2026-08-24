from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QDialogButtonBox, QLabel, QComboBox)
from PyQt6.QtCore import Qt

#  Ajout des imports CHOIX_COLONNES et STYLE_EDIT_COMBOBOX
from config import (STYLE_EDIT_DIALOG, STYLE_EDIT_BUTTONS, STYLE_READONLY_INPUT, 
                    CHOIX_COLONNES, STYLE_EDIT_COMBOBOX)

class EditAffaireDialog(QDialog):
    def __init__(self, row_data, colonnes_a_afficher, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Modifier l'affaire : {row_data.get('NOM', 'Inconnue')}")
        self.resize(450, 500)
        
        self.setStyleSheet(STYLE_EDIT_DIALOG)

        self.row_data = row_data
        self.inputs = {} 

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        for col_back, col_front in colonnes_a_afficher.items():
            valeur = str(row_data.get(col_back, "")).strip()
            
            if valeur.endswith(".0"): valeur = valeur[:-2]
            if valeur.lower() in ["nan", "n/a", "none"]: valeur = ""
            
            # --- CRÉATION DYNAMIQUE : Liste déroulante OU Champ texte ---
            if col_back in CHOIX_COLONNES:
                champ = QComboBox()
                champ.setStyleSheet(STYLE_EDIT_COMBOBOX)
                champ.addItems(CHOIX_COLONNES[col_back])
                
                # On place le menu sur la valeur actuelle du fichier
                index = champ.findText(valeur)
                if index >= 0:
                    champ.setCurrentIndex(index)
                elif valeur: 
                    champ.addItem(valeur)
                    champ.setCurrentText(valeur)
            else:
                champ = QLineEdit(valeur)
                if col_back in ["NOM", "CHORUS PRO"]:
                    champ.setReadOnly(True)
                    champ.setStyleSheet(STYLE_READONLY_INPUT)
                
            self.inputs[col_back] = champ
            form_layout.addRow(QLabel(col_front + " :"), champ)

        layout.addLayout(form_layout)

        self.btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btn_box.setStyleSheet(STYLE_EDIT_BUTTONS)
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)
        
        layout.addStretch()
        layout.addWidget(self.btn_box)

    def get_new_data(self):
        """Récupère les données et convertit les nombres pour éviter l'erreur dtype de Pandas."""
        new_data = {}
        for col_back, champ in self.inputs.items():
            
            # Extraction du texte selon le type de composant
            if isinstance(champ, QComboBox):
                valeur_texte = champ.currentText().strip()
            else:
                valeur_texte = champ.text().strip()
                
            # --- CONVERSION NUMÉRIQUE POUR PANDAS ---
            if valeur_texte.isdigit():
                valeur_finale = int(valeur_texte)
            else:
                try:
                    valeur_finale = float(valeur_texte)
                except ValueError:
                    valeur_finale = valeur_texte # On laisse en texte pur
                    
            new_data[col_back] = valeur_finale
            
        return new_data