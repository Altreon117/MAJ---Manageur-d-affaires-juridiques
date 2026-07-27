from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel
from PyQt6.QtCore import Qt

class CardJAFComponent(QFrame):
    def __init__(self, row_data, colonnes_a_afficher):
        super().__init__()
        
        self.setObjectName("card_jaf")
        # On peut réduire un peu la hauteur minimum vu que ça prendra moins de place en hauteur
        self.setMinimumHeight(100) 
        
        # --- DONNÉES BACKEND DISPONIBLES (Invisibles) ---
        self.planification_cachee = str(row_data.get("Planification", ""))
        
        # --- GÉNÉRATION DU FRONTEND (Affichage dynamique en grille) ---
        # 💡 Remplacement du QVBoxLayout par un QGridLayout
        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setHorizontalSpacing(50) # Espace horizontal entre les 2 colonnes
        layout.setVerticalSpacing(10)   # Espace vertical entre les lignes
        
        # On utilise "enumerate" pour avoir à la fois le numéro (index) et le nom de la colonne
        for index, col_name in enumerate(colonnes_a_afficher):
            # On récupère la valeur correspondante dans la donnée backend
            valeur = str(row_data.get(col_name, "N/A")).strip()
            
            # On crée un label dynamique
            lbl = QLabel(f"<b>{col_name}</b> : {valeur}")
            lbl.setStyleSheet("border: none; font-size: 14px;")
            
            # Si c'est le "NOM", on le met en bleu
            if col_name == "NOM":
                lbl.setStyleSheet("border: none; font-size: 16px; color: #1877F2;")
                
            # 💡 Calcul de la position dans la grille :
            # Si index = 0 -> Ligne 0, Colonne 0
            # Si index = 1 -> Ligne 0, Colonne 1
            # Si index = 2 -> Ligne 1, Colonne 0 ...
            row = index // 2
            col = index % 2
            
            layout.addWidget(lbl, row, col)