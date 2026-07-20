from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt

class DashBoardView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # --- CRÉATION DU TABLEAU ---
        # 1. Cadre externe
        self.board_ext_frame = QFrame()
        self.board_ext_frame.setObjectName("board_ext_frame")
        
        # Layout interne du cadre externe
        ext_layout = QVBoxLayout(self.board_ext_frame)
        ext_layout.setContentsMargins(20, 20, 20, 20)
        
        # 2. Interne du cadre 
        self.board_int_frame = QFrame()
        self.board_int_frame.setObjectName("board_int_frame")
        
        # Layout interne du cadre interne
        int_layout = QVBoxLayout(self.board_int_frame)
        int_layout.setContentsMargins(20, 20, 20, 20)
        
        titre = QLabel("DASHBOARD")
        titre.setStyleSheet("font-size: 24px; font-weight: bold;")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        int_layout.addWidget(titre)
        
        ext_layout.addWidget(self.board_int_frame)
        
        layout.addWidget(self.board_ext_frame)