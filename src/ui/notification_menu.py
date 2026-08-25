from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from config import STYLE_NOTIFICATION_EMPTY, STYLE_NOTIFICATION_MENU

# Import du composant séparé
from src.ui.card_mission_component import MissionCard

class NotificationMenu(QFrame):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window 

        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(STYLE_NOTIFICATION_MENU)
        self.setFixedWidth(350)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self.lbl_vide = QLabel("Aucune nouvelle mission.")
        self.lbl_vide.setStyleSheet(STYLE_NOTIFICATION_EMPTY)
        self.layout.addWidget(self.lbl_vide)
        
    def peupler_missions(self, liste_missions):
        """Nettoie le menu et le remplit avec les cartes."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
                
        if not liste_missions:
            self.layout.addWidget(self.lbl_vide)
            self.lbl_vide.show()
            self.adjustSize()
            return
            
        for mission in liste_missions:
            carte = MissionCard(mission, self)
            self.layout.addWidget(carte)
            
        self.adjustSize()

    def verifier_etat_vide(self):
        """Vérifie s'il reste des cartes après une suppression (Refus)."""
        if self.layout.count() == 0:
            self.layout.addWidget(self.lbl_vide)
            self.lbl_vide.show()
            
            # Éteint la cloche dans le header
            if hasattr(self.main_window, "mettre_a_jour_icone_cloche"):
                self.main_window.mettre_a_jour_icone_cloche(False)
                
        self.adjustSize()