from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt

class CardJAFComponent(QFrame):
    def __init__(self, row_data, colonnes_a_afficher):
        super().__init__()
        
        # On sauvegarde les données brutes dans l'objet pour la barre de recherche
        self.row_data = row_data 
        
        self.setObjectName("card_jaf")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # --- GÉNÉRATION DU FRONTEND (Affichage dynamique en grille) ---
        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setHorizontalSpacing(50) 
        layout.setVerticalSpacing(10)   
        
        for index, col_name in enumerate(colonnes_a_afficher):
            valeur = str(row_data.get(col_name, "N/A")).strip()
            
            lbl = QLabel(f"<b>{col_name}</b> : {valeur}")
            
            if col_name == "NOM":
                lbl.setObjectName("card_label_nom")
            else:
                lbl.setObjectName("card_label_normal")
                
            row = index // 2
            col = index % 2
            
            layout.addWidget(lbl, row, col)

    # Le moteur de recherche interne de la carte
    def correspond_a_la_recherche(self, texte_recherche):
        """Retourne True si le texte cherché se trouve dans les données de cette carte."""
        if not texte_recherche:
            return True 
            
        texte_min = texte_recherche.lower()
        
        for valeur in self.row_data.values():
            if texte_min in str(valeur).lower():
                return True
                
        return False