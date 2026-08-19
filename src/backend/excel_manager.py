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
        
    @staticmethod
    def update_payments(update_filepath):
        """Lit le fichier de mise à jour et passe l'État 2 à 'payé' pour les affaires trouvées."""
        try:
            # 1. Lecture du fichier de mise à jour
            df_update = pd.read_excel(update_filepath)
            
            # On vérifie que la colonne Note existe bien
            if 'Note' not in df_update.columns:
                return -1 
                
            # On extrait tous les numéros de la colonne Note (en ignorant les cases vides)
            notes_payees = df_update['Note'].dropna().astype(str).str.strip().tolist()
            if not notes_payees:
                return 0
                
            total_updated = 0
            
            # 2. On met à jour les 3 fichiers découpés ET le fichier MAÎTRE
            fichiers_a_mettre_a_jour = [EXCEL_FILE, OPJ_EXCEL_FILE, JAF_EXCEL_FILE, JI_EXCEL_FILE]
            
            for fichier in fichiers_a_mettre_a_jour:
                if os.path.exists(fichier):
                    df = pd.read_excel(fichier)
                    
                    # On vérifie que les colonnes nécessaires existent dans ce fichier
                    if 'CHORUS PRO' in df.columns and 'État 2' in df.columns:
                        # Nettoyage de la colonne pour comparer proprement
                        chorus_col = df['CHORUS PRO'].astype(str).str.strip()
                        
                        # Le masque : Le CHORUS PRO est dans les Notes ET n'est pas déjà 'payé'
                        mask = chorus_col.isin(notes_payees) & (df['État 2'].astype(str).str.lower().str.strip() != 'payé')
                        
                        nombre_modifications = mask.sum()
                        if nombre_modifications > 0:
                            df.loc[mask, 'État 2'] = 'payé'
                            df.to_excel(fichier, index=False)
                            
                            # On ne compte le total que sur les fichiers découpés (pour ne pas compter le maître en double)
                            if fichier != EXCEL_FILE:
                                total_updated += nombre_modifications

            return total_updated
            
        except Exception as e:
            print(f"Erreur critique lors de la mise à jour des paiements : {e}")
            return -1
        
    @staticmethod
    def get_dashboard_metrics():
        """Calcule et retourne les métriques pour le dashboard sous forme de dictionnaire."""
        metrics = {
            "total_opj": 0, "total_jaf": 0, "total_ji": 0,
            "attente_paiement": 0, "montant_total": 0,
            "rapports_a_faire": 0, "affaires_terminees": 0, "chorus_manquants": 0
        }
        
        try:
            dfs = []
            
            # 1. Récupération des totaux par service
            if os.path.exists(OPJ_EXCEL_FILE):
                df_opj = pd.read_excel(OPJ_EXCEL_FILE)
                metrics["total_opj"] = len(df_opj)
                dfs.append(df_opj)
                
            if os.path.exists(JAF_EXCEL_FILE):
                df_jaf = pd.read_excel(JAF_EXCEL_FILE)
                metrics["total_jaf"] = len(df_jaf)
                dfs.append(df_jaf)
                
            if os.path.exists(JI_EXCEL_FILE):
                df_ji = pd.read_excel(JI_EXCEL_FILE)
                metrics["total_ji"] = len(df_ji)
                dfs.append(df_ji)
                
            # 2. Fusion pour les calculs globaux
            if dfs:
                df_global = pd.concat(dfs, ignore_index=True)
                
                # Dossiers en attente de paiement (État 2)
                if 'État 2' in df_global.columns:
                    etat2 = df_global['État 2'].astype(str).str.strip().str.lower()
                    metrics["attente_paiement"] = len(df_global[~etat2.isin(['payé', 'nan', '', 'n/a'])])
                    
                # Montant total facturé
                if 'montant' in df_global.columns:
                    montants = pd.to_numeric(df_global['montant'], errors='coerce').fillna(0)
                    metrics["montant_total"] = int(montants.sum())
                    
                # Rapports à faire / Terminés (État)
                if 'État' in df_global.columns:
                    etat = df_global['État'].astype(str).str.strip().str.lower()
                    metrics["rapports_a_faire"] = len(df_global[etat.isin(['a faire', 'à faire', 'pas commencé'])])
                    metrics["affaires_terminees"] = len(df_global[etat == 'terminé'])
                    
                # Chorus manquants
                if 'CHORUS PRO' in df_global.columns:
                    chorus = df_global['CHORUS PRO'].astype(str).str.strip().str.lower()
                    metrics["chorus_manquants"] = len(df_global[chorus.isin(['nan', '', 'n/a'])])
                    
        except Exception as e:
            print(f"Erreur lors du calcul des métriques du dashboard : {e}")
            
        return metrics