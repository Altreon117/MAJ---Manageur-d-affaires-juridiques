import os
import re
import datetime
from imap_tools import MailBox, AND
from dotenv import load_dotenv

class MailConnector:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("EMAIL_COMPTE")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.imap_server = 'imap.gmail.com'
        
        # Définition d'une date de départ fixe (année, mois, jour)
        # Le logiciel cherchera toujours les mails non lus depuis cette date.
        self.date_initialisation = datetime.date(2026, 8, 1)

    def check_new_missions(self, missions_refusees):
        if not self.email or not self.password:
            return []

        nouvelles_missions = []
        try:
            with MailBox(self.imap_server).login(self.email, self.password) as mailbox:
                # Suppression de 'seen=False' et ajout de 'mark_seen=False'
                criteres = AND(date_gte=self.date_initialisation)
                
                for msg in mailbox.fetch(criteres, mark_seen=False):
                    sujet = msg.subject
                    if sujet.upper().startswith("MISSION") and sujet not in missions_refusees:
                        nouvelles_missions.append({
                            "sujet": sujet,
                            "date": msg.date.strftime("%d/%m/%Y"),
                            "uid": msg.uid
                        })
        except Exception as e:
            print(f"Erreur IMAP : {e}")
            
        return nouvelles_missions