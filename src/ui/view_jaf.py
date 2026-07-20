from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class JAFView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        titre = QLabel("Gestion des expertises JAF")
        titre.setStyleSheet("font-size: 24px; font-weight: bold;")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(titre)