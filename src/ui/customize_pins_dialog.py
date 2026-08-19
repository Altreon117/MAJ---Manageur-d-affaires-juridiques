from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, QCheckBox, 
                             QDialogButtonBox, QLabel, QMessageBox, QFrame)
from PyQt6.QtCore import Qt

from config import DASHBOARD_AVAILABLE_PINS

class CustomizePinsDialog(QDialog):
    def __init__(self, current_active_pins, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Personnaliser le Dashboard")
        self.setFixedSize(500, 350)
        
        # Le style de la fenêtre (fond gris clair)
        self.setStyleSheet("""
            QDialog { background-color: #F5F6FA; }
            QLabel { color: #000000; font-family: 'Segoe UI', Arial, sans-serif; }
            QCheckBox { color: #000000; font-size: 14px; padding: 5px; }
            
            QCheckBox::indicator { 
                width: 18px; 
                height: 18px; 
                border-radius: 9px; 
                border: 2px solid #A4ACAFFF; 
                background-color: #FFFFFF;
            }
            QCheckBox::indicator:checked { 
                background-color: #bca0dc; 
                border: 2px solid #bca0dc; 
            }
        """)

        self.ordered_selection = current_active_pins.copy()
        self.checkboxes = {}

        self.setup_ui()
        self.mettre_a_jour_numeros() # Affiche les numéros au lancement

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- EN-TÊTE ---
        titre = QLabel("Sélectionnez et ordonnez les indicateurs :")
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        sous_titre = QLabel("<i>(Maximum 6. L'ordre de vos clics définit l'ordre d'affichage)</i>")
        sous_titre.setStyleSheet("color: gray; font-size: 13px;")

        layout.addWidget(titre)
        layout.addWidget(sous_titre)

        # --- CORPS : Grille de Checkboxes ---
        frame_grid = QFrame()
        frame_grid.setStyleSheet("background-color: #FFFFFF; border: 1px solid #A4ACAFFF; border-radius: 8px;")
        grid_layout = QGridLayout(frame_grid)
        grid_layout.setContentsMargins(15, 15, 15, 15)
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setVerticalSpacing(15)

        # Génération dynamique à partir de DASHBOARD_AVAILABLE_PINS
        for index, (pin_key, pin_name) in enumerate(DASHBOARD_AVAILABLE_PINS.items()):
            checkbox = QCheckBox(pin_name)
            
            if pin_key in self.ordered_selection:
                checkbox.setChecked(True)
                
            checkbox.clicked.connect(lambda checked, pk=pin_key: self.gerer_clic(checked, pk))
            
            self.checkboxes[pin_key] = checkbox
            
            row = index // 2
            col = index % 2
            grid_layout.addWidget(checkbox, row, col)

        layout.addWidget(frame_grid)
        layout.addStretch()

        # --- PIED DE PAGE : Boutons Save/Cancel ---
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF; border: 1px solid #A4ACAFFF; 
                border-radius: 15px; padding: 5px 15px; font-weight: bold;
            }
            QPushButton:hover { border: 1px solid #bca0dc; color: #bca0dc; }
        """)
        
        self.button_box.accepted.connect(self.save_selection)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def gerer_clic(self, checked, pin_key):
        """Gère l'ajout et le retrait des indicateurs avec vérification stricte."""
        if checked:
            # 1. L'utilisateur coche une case : On vérifie la limite
            if len(self.ordered_selection) >= 6:
                QMessageBox.warning(self, "Limite atteinte", "Vous ne pouvez pas sélectionner plus de 6 indicateurs simultanément.")
                
                # On annule le clic proprement pour bloquer le 7ème
                cb = self.checkboxes[pin_key]
                cb.blockSignals(True) 
                cb.setChecked(False)
                cb.blockSignals(False)
                return
                
            # 2. Si c'est bon, on l'ajoute à la fin de notre liste ordonnée
            self.ordered_selection.append(pin_key)
            
        else:
            # 3. L'utilisateur décoche une case : On la retire de l'ordre
            if pin_key in self.ordered_selection:
                self.ordered_selection.remove(pin_key)
                
        # 4. On rafraîchit l'affichage des numéros
        self.mettre_a_jour_numeros()

    def mettre_a_jour_numeros(self):
        """Ajoute un numéro devant le texte pour montrer l'ordre de sélection."""
        for pin_key, cb in self.checkboxes.items():
            nom_original = DASHBOARD_AVAILABLE_PINS[pin_key]
            
            if pin_key in self.ordered_selection:
                position = self.ordered_selection.index(pin_key) + 1
                cb.setText(f"{position}. {nom_original}")
            else:
                cb.setText(nom_original)

    def save_selection(self):
        """Valide et ferme la fenêtre."""
        if len(self.ordered_selection) == 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner au moins un indicateur.")
            return
            
        self.accept()

    def get_selected_pins(self):
        """Retourne la liste finale triée par l'utilisateur."""
        return self.ordered_selection