import pandas as pd
import numpy as np
import os
from config import EXCEL_FILE, OPJ_EXCEL_FILE, JAF_EXCEL_FILE

class ExcelManager:
    @staticmethod
    def split_master_file():
        """
        Vérifie si le fichier global (maître) existe, le divise en deux DataFrames (OPJ et JAF),
        et sauvegarde physiquement les deux nouveaux fichiers Excel.
        """
        if not os.path.exists(EXCEL_FILE):
            print(f"Erreur : Le fichier global '{EXCEL_FILE}' est introuvable.")
            return False

        try:
            print("Découpage du fichier global en cours...")
            df = pd.read_excel(EXCEL_FILE)
            
            # Vérification de la présence de la colonne de référence
            if 'REF AFFAIRE' not in df.columns:
                print("Erreur : La colonne 'REF AFFAIRE' est introuvable dans le fichier global.")
                return False

            # Création d'une colonne temporaire propre pour le filtrage (majuscules, sans espaces)
            df['REF_TEMP'] = df['REF AFFAIRE'].astype(str).str.strip().str.upper()
            
            # Filtrage des données
            df_opj = df[df['REF_TEMP'] == 'OPJ'].copy()
            df_jaf = df[df['REF_TEMP'] == 'JAF'].copy()
            
            # Nettoyage de la colonne temporaire
            df_opj = df_opj.drop(columns=['REF_TEMP'])
            df_jaf = df_jaf.drop(columns=['REF_TEMP'])
            
            # Sauvegarde des deux nouveaux fichiers physiques
            df_opj.to_excel(OPJ_EXCEL_FILE, index=False)
            df_jaf.to_excel(JAF_EXCEL_FILE, index=False)
            
            print("Génération réussie : Fichiers OPJ et JAF créés !")
            return True

        except Exception as e:
            print(f"Erreur critique lors de la division du fichier global : {e}")
            return False

    @staticmethod
    def read_sheet(affaire_type):
        """
        Vérifie la présence des fichiers découpés. S'ils manquent, lance la découpe.
        Puis lit les données depuis le fichier découpé demandé.
        """
        # 1. Vérification de l'existence des DEUX fichiers découpés
        fichiers_manquants = not (os.path.exists(OPJ_EXCEL_FILE) and os.path.exists(JAF_EXCEL_FILE))
        
        if fichiers_manquants:
            # S'il en manque au moins un, on déclenche le processus de création
            succes_creation = ExcelManager.split_master_file()
            if not succes_creation:
                # Si la création échoue (ex: pas de fichier d'origine), on arrête tout
                return []

        # 2. Détermination du fichier cible (qui existe forcément maintenant)
        specific_file = OPJ_EXCEL_FILE if affaire_type == "OPJ" else JAF_EXCEL_FILE

        try:
            # 3. Lecture du fichier spécifique
            df = pd.read_excel(specific_file)
            
            # 4. Nettoyage robuste (remplace les cases vides et dates vides par "")
            df = df.replace({np.nan: "", pd.NaT: ""})
            
            # 5. Conversion en liste de dictionnaires pour l'interface
            lignes = df.to_dict(orient='records')
            return lignes

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {specific_file} : {e}")
            return []