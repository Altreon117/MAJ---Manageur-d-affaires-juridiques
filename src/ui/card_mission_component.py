from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
import webbrowser

from src.backend.excel_manager import ExcelManager
from config import (
    STYLE_MISSION_BUTTON_ACCEPT,
    STYLE_MISSION_BUTTON_REFUSE,
    STYLE_MISSION_BUTTON_VIEW,
    STYLE_MISSION_CARD,
)
from src.ui.add_affaire_dialog import AddAffaireDialog

class MissionCard(QFrame):
    def __init__(self, mission_data, parent_menu):
        super().__init__()
        self.mission_data = mission_data
        self.parent_menu = parent_menu

        self.setStyleSheet(STYLE_MISSION_CARD)
        
        layout = QVBoxLayout(self)
        
        # Textes
        lbl_titre = QLabel(f"<b>Nouvelle mission :</b> {mission_data['sujet']}")
        lbl_titre.setWordWrap(True) # Force le retour à la ligne
        
        lbl_date = QLabel(f"<i>Date : {mission_data['date']}</i>")
        
        layout.addWidget(lbl_titre)
        layout.addWidget(lbl_date)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        btn_voir = QPushButton("Voir")
        btn_voir.setStyleSheet(STYLE_MISSION_BUTTON_VIEW)
        btn_voir.clicked.connect(self.ouvrir_mail)

        btn_accepter = QPushButton("Accepter")
        btn_accepter.setStyleSheet(STYLE_MISSION_BUTTON_ACCEPT)
        btn_accepter.clicked.connect(self.accepter_mission)

        btn_refuser = QPushButton("Refuser")
        btn_refuser.setStyleSheet(STYLE_MISSION_BUTTON_REFUSE)
        btn_refuser.clicked.connect(self.refuser_mission)
        
        btn_layout.addWidget(btn_voir)
        btn_layout.addWidget(btn_accepter)
        btn_layout.addWidget(btn_refuser)
        layout.addLayout(btn_layout)

    def ouvrir_mail(self):
        """Ouvre Gmail dans le navigateur web par défaut."""
        webbrowser.open(f"https://mail.google.com/mail/u/0/#search/{self.mission_data['sujet']}")

    def accepter_mission(self):
        self.parent_menu.hide()
        
        sujet_mail = self.mission_data['sujet']
        dialog = AddAffaireDialog(sujet_mail, self.window())
        
        if dialog.exec():
            type_affaire, nouvelles_donnees = dialog.get_data()
            succes = ExcelManager.add_affaire(type_affaire, nouvelles_donnees)
            
            fenetre_principale = self.window()
            
            if succes:
                ExcelManager.remove_notification(sujet_mail)
                ExcelManager.add_refused_mission(sujet_mail, self.mission_data['date'])
                
                self.setParent(None)
                self.parent_menu.verifier_etat_vide()
                
                if hasattr(fenetre_principale, "afficher_notification"):
                    fenetre_principale.afficher_notification(f"Succès : L'affaire a été créée dans {type_affaire} !")
                    fenetre_principale.page_opj.charger_donnees_excel()
                    fenetre_principale.page_jaf.charger_donnees_excel()
                    fenetre_principale.page_ji.charger_donnees_excel()
                    fenetre_principale.page_accueil.generer_cartes()

    def refuser_mission(self):
        sujet_mail = self.mission_data['sujet']
        ExcelManager.remove_notification(sujet_mail)
        ExcelManager.add_refused_mission(sujet_mail, self.mission_data['date'])
        
        self.setParent(None)
        self.parent_menu.verifier_etat_vide()