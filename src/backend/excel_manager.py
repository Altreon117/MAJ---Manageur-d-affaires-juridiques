import pandas as pd
import numpy as np
import os
from config import EXCEL_FILE, OPJ_EXCEL_FILE, JAF_EXCEL_FILE, JI_EXCEL_FILE

class ExcelManager:
    @staticmethod
    def split_master_file():
        # Vérifie si le fichier global (maître) existe, le divise en trois DataFrames (OPJ, JAF, JI)
        if not os.path.exists(EXCEL_FILE):
            print(f"Erreur : Le fichier global '{EXCEL_FILE}' est introuvable.")
            return False

        try:
            print("Découpage, fusion et nettoyage des onglets en cours...")
            
            # Lecture de tous les onglets
            all_sheets = pd.read_excel(EXCEL_FILE, sheet_name=None)
            
            # Fusion de tous les onglets en un seul tableau
            df = pd.concat(all_sheets.values(), ignore_index=True)
            
            # 💡 NOUVEAU : SYSTÈME ANTI-DOUBLONS
            # On détermine les colonnes qui servent à identifier un doublon
            colonnes_criteres = []
            if 'NOM' in df.columns:
                colonnes_criteres.append('NOM')
            if 'CHORUS PRO' in df.columns:
                colonnes_criteres.append('CHORUS PRO')
                
            # Si on a au moins une colonne de critère, on nettoie le tableau
            if colonnes_criteres:
                # keep='first' garde la première apparition et supprime les copies suivantes
                df = df.drop_duplicates(subset=colonnes_criteres, keep='first')
            
            # Vérification de la présence de la colonne de référence
            if 'REF AFFAIRE' not in df.columns:
                print("Erreur : La colonne 'REF AFFAIRE' est introuvable dans le fichier.")
                return False

            # Création d'une colonne temporaire propre pour le filtrage
            df['REF_TEMP'] = df['REF AFFAIRE'].astype(str).str.strip().str.upper()
            
            # Filtrage des données
            df_opj = df[df['REF_TEMP'] == 'OPJ'].copy()
            df_jaf = df[df['REF_TEMP'] == 'JAF'].copy()
            df_ji = df[df['REF_TEMP'] == 'JI'].copy()
            
            # Nettoyage de la colonne temporaire
            df_opj = df_opj.drop(columns=['REF_TEMP'])
            df_jaf = df_jaf.drop(columns=['REF_TEMP'])
            df_ji = df_ji.drop(columns=['REF_TEMP'])
            
            # Sauvegarde des fichiers physiques
            df_opj.to_excel(OPJ_EXCEL_FILE, index=False)
            df_jaf.to_excel(JAF_EXCEL_FILE, index=False)
            df_ji.to_excel(JI_EXCEL_FILE, index=False)
            
            print("Génération réussie : Fichiers OPJ, JAF et JI mis à jour et sans doublons !")
            return True

        except Exception as e:
            print(f"Erreur critique lors de la division du fichier global : {e}")
            return False

    @staticmethod
    def read_sheet(affaire_type, colonnes_souhaitees=None):
        besoin_maj = False
        
        # 1. Vérification de l'existence des fichiers
        if not (os.path.exists(OPJ_EXCEL_FILE) and os.path.exists(JAF_EXCEL_FILE) and os.path.exists(JI_EXCEL_FILE)):
            besoin_maj = True
        
        # 2. VÉRIFICATION DE CACHE : Le fichier maître a-t-il été modifié récemment ?
        elif os.path.exists(EXCEL_FILE):
            temps_master = os.path.getmtime(EXCEL_FILE)
            temps_ji = os.path.getmtime(JI_EXCEL_FILE)
            
            if temps_master > temps_ji:
                print("Modifications détectées dans le fichier Excel d'origine. Mise à jour en cours...")
                besoin_maj = True

        # Déclenchement de la mise à jour si nécessaire
        if besoin_maj:
            succes_creation = ExcelManager.split_master_file()
            if not succes_creation:
                return []

        # Détermination du fichier cible
        specific_file = OPJ_EXCEL_FILE if affaire_type == "OPJ" else JAF_EXCEL_FILE if affaire_type == "JAF" else JI_EXCEL_FILE

        try:
            df = pd.read_excel(specific_file)
            
            if colonnes_souhaitees:
                colonnes_presentes = [col for col in colonnes_souhaitees if col in df.columns]
                df = df[colonnes_presentes]
            
            df = df.replace({np.nan: "", pd.NaT: ""})
            lignes = df.to_dict(orient='records')
            return lignes

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {specific_file} : {e}")
            return []