from PyQt6.QtWidgets import QFrame, QHBoxLayout, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

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
        tri_layout = QVBoxLayout(self.tri_frame)
        tri_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_recherche = QLabel("RECHERCHER :")
        lbl_tri = QLabel("TRIER PAR :")
        lbl_recherche.setStyleSheet("font-size: 16px;")
        lbl_tri.setStyleSheet("font-size: 16px;")
        
        tri_layout.addWidget(lbl_recherche)
        tri_layout.addWidget(lbl_tri)
        
        # --- PARTIE DROITE BASSE - LITTLE BODY ---
        self.little_body_widget = QWidget()
        little_layout = QVBoxLayout(self.little_body_widget)
        little_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_liste = QLabel("[ Zone des futures cartes de dossiers ]")
        lbl_liste.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_liste.setStyleSheet("color: gray;")
        
        little_layout.addWidget(lbl_liste)
        little_layout.addStretch()
        
        # --- ASSEMBLAGE DE LA PARTIE DROITE ---
        grand_body_layout.addWidget(self.tri_frame, 1)
        grand_body_layout.addWidget(self.little_body_widget, 4)
        
        # --- ASSEMBLAGE FINAL DE LA PAGE ---
        main_layout.addWidget(self.filter_frame, 1) 
        main_layout.addWidget(self.grand_body_frame, 4)