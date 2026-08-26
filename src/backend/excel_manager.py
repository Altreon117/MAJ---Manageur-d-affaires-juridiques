import pandas as pd
import numpy as np
import os
from config import EXCEL_FILE, NOTIFICATIONS_EXCEL_FILE, OPJ_EXCEL_FILE, JAF_EXCEL_FILE, JI_EXCEL_FILE, REFUS_EXCEL_FILE

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
            
            # Système anti-doublons
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
        """Lit le fichier bancaire, extrait les CHORUS PRO, et passe l'État 2 à 'payé'."""
        try:
            # 1. Lecture du fichier de mise à jour
            df_update = pd.read_excel(update_filepath)
            
            # On vérifie la présence de la NOUVELLE colonne
            if 'Référence' not in df_update.columns:
                return -1 
                
            # Extraction du motif "MJ" suivi de chiffres
            # r'(MJ\d+)' signifie : "Trouve 'MJ' collé à un ou plusieurs chiffres (\d+), et capture-le"
            extracted_refs = df_update['Référence'].astype(str).str.extract(r'(MJ\d+)', expand=False)
            
            # On supprime les lignes qui ne contenaient pas de "MJ..." (devenues NaN) et on convertit en liste
            notes_payees = extracted_refs.dropna().str.strip().tolist()
            
            if not notes_payees:
                return 0
                
            total_updated = 0
            
            # 2. On met à jour les 3 fichiers découpés ET le fichier MAÎTRE
            fichiers_a_mettre_a_jour = [EXCEL_FILE, OPJ_EXCEL_FILE, JAF_EXCEL_FILE, JI_EXCEL_FILE]
            
            for fichier in fichiers_a_mettre_a_jour:
                if os.path.exists(fichier):
                    df = pd.read_excel(fichier)
                    
                    if 'CHORUS PRO' in df.columns and 'État 2' in df.columns:
                        chorus_col = df['CHORUS PRO'].astype(str).str.strip()
                        
                        mask = chorus_col.isin(notes_payees) & (df['État 2'].astype(str).str.lower().str.strip() != 'payé')
                        
                        nombre_modifications = mask.sum()
                        if nombre_modifications > 0:
                            df.loc[mask, 'État 2'] = 'payé'
                            df.to_excel(fichier, index=False)
                            
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
            # Si les fichiers séparés n'existent pas, on force leur recréation avant de compter !
            fichiers_manquants = not (os.path.exists(OPJ_EXCEL_FILE) and os.path.exists(JAF_EXCEL_FILE) and os.path.exists(JI_EXCEL_FILE))
            if fichiers_manquants:
                ExcelManager.split_master_file()
            
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
    
    @staticmethod
    def update_row(onglet_nom, original_data, new_data):
        """Met à jour une ligne en utilisant CHORUS PRO en priorité absolue, ou le NOM en solution de repli (ex: JAF)."""
        try:
            # 1. Identification du fichier cible
            fichier_cible = None
            if onglet_nom == "OPJ":
                fichier_cible = OPJ_EXCEL_FILE
            elif onglet_nom == "JAF":
                fichier_cible = JAF_EXCEL_FILE
            elif onglet_nom == "JI":
                fichier_cible = JI_EXCEL_FILE

            # Extraction des données clés (get renvoie "" si la colonne n'existe pas, comme pour JAF)
            chorus_ref = original_data.get("CHORUS PRO", "")
            nom_affaire = original_data.get("NOM", "")

            # --- MOTEUR DE RECHERCHE EN CASCADE ---
            def obtenir_masque_de_recherche(dataframe):
                # NIVEAU 1 : Vérification de la présence du CHORUS PRO (OPJ, JI)
                if chorus_ref and str(chorus_ref).strip().lower() not in ["", "nan", "n/a", "none"]:
                    if "CHORUS PRO" in dataframe.columns:
                        return dataframe["CHORUS PRO"].astype(str).str.strip() == str(chorus_ref).strip()
                
                # NIVEAU 2 : Repli sur le NOM (JAF utilise exclusivement ce niveau)
                if nom_affaire and str(nom_affaire).strip().lower() not in ["", "nan", "n/a", "none"]:
                    if "NOM" in dataframe.columns:
                        return dataframe["NOM"].astype(str).str.strip() == str(nom_affaire).strip()
                        
                return None
            # ----------------------------------------

            # 2. Application des modifications sur le fichier découpé
            if fichier_cible and os.path.exists(fichier_cible):
                df = pd.read_excel(fichier_cible)
                mask = obtenir_masque_de_recherche(df)
                
                if mask is not None and mask.any():
                    for col, val in new_data.items():
                        if col in df.columns:
                            df.loc[mask, col] = val
                    df.to_excel(fichier_cible, index=False)

            # 3. Synchronisation avec le fichier MAÎTRE global
            if os.path.exists(EXCEL_FILE):
                df_master = pd.read_excel(EXCEL_FILE)
                mask_master = obtenir_masque_de_recherche(df_master)
                
                if mask_master is not None and mask_master.any():
                    for col, val in new_data.items():
                        if col in df_master.columns:
                            df_master.loc[mask_master, col] = val
                    df_master.to_excel(EXCEL_FILE, index=False)
                    
            return True
            
        except Exception as e:
            print(f"Erreur critique lors de la modification de l'affaire : {e}")
            return False
        
    @staticmethod
    def get_refused_missions():
        """Retourne la liste des sujets de missions refusées. Crée le fichier s'il n'existe pas."""
        # Création automatique du fichier s'il est manquant
        if not os.path.exists(REFUS_EXCEL_FILE):
            df_vide = pd.DataFrame(columns=["Sujet", "Date"])
            try:
                df_vide.to_excel(REFUS_EXCEL_FILE, index=False)
                return []
            except Exception as e:
                print(f"Erreur lors de la création du fichier de refus : {e}")
                return []
                
        # Lecture classique si le fichier existe
        df = pd.read_excel(REFUS_EXCEL_FILE)
        if "Sujet" in df.columns:
            return df["Sujet"].tolist()
        return []

    @staticmethod
    def add_refused_mission(sujet, date_mail):
        """Ajoute une mission à la liste noire des refus."""
        nouvelle_ligne = {"Sujet": sujet, "Date": date_mail}
        
        if os.path.exists(REFUS_EXCEL_FILE):
            df = pd.read_excel(REFUS_EXCEL_FILE)
            df = pd.concat([df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
        else:
            df = pd.DataFrame([nouvelle_ligne])
            
        df.to_excel(REFUS_EXCEL_FILE, index=False)
        
    @staticmethod
    def add_affaire(onglet_nom, new_data):
        """Ajoute une nouvelle affaire dans le fichier spécifique ET dans le fichier maître."""
        try:
            fichier_cible = None
            if onglet_nom == "OPJ":
                fichier_cible = OPJ_EXCEL_FILE
            elif onglet_nom == "JAF":
                fichier_cible = JAF_EXCEL_FILE
            elif onglet_nom == "JI":
                fichier_cible = JI_EXCEL_FILE

            # 1. Ajout dans le fichier découpé (s'il existe)
            if fichier_cible and os.path.exists(fichier_cible):
                df = pd.read_excel(fichier_cible)
                # On transforme le dictionnaire en DataFrame d'une ligne pour l'ajouter proprement
                df_new = pd.DataFrame([new_data])
                df = pd.concat([df, df_new], ignore_index=True)
                df.to_excel(fichier_cible, index=False)

            # 2. Ajout dans le fichier MAÎTRE (très important)
            if os.path.exists(EXCEL_FILE):
                df_master = pd.read_excel(EXCEL_FILE)
                
                # Pour le fichier maître, on DOIT renseigner la colonne 'REF AFFAIRE' 
                # sinon il sera perdu à la prochaine découpe !
                new_data_master = new_data.copy()
                new_data_master['REF AFFAIRE'] = onglet_nom
                
                df_new_master = pd.DataFrame([new_data_master])
                df_master = pd.concat([df_master, df_new_master], ignore_index=True)
                df_master.to_excel(EXCEL_FILE, index=False)
                
            return True
        except Exception as e:
            print(f"Erreur critique lors de la création de l'affaire : {e}")
            return False
        
    @staticmethod
    def get_cached_notifications():
        """Récupère les notifications stockées localement. Crée le fichier si absent."""
        import datetime
        if not os.path.exists(NOTIFICATIONS_EXCEL_FILE):
            df_vide = pd.DataFrame(columns=["sujet", "date", "uid"])
            df_vide.to_excel(NOTIFICATIONS_EXCEL_FILE, index=False)
            return []
            
        df = pd.read_excel(NOTIFICATIONS_EXCEL_FILE)
        df = df.replace({np.nan: ""})
        return df.to_dict(orient='records')

    @staticmethod
    def get_latest_notification_date():
        """Trouve la date du mail le plus récent dans le cache, ou retourne le 01/08/2026 par défaut."""
        import datetime
        if os.path.exists(NOTIFICATIONS_EXCEL_FILE):
            df = pd.read_excel(NOTIFICATIONS_EXCEL_FILE)
            if not df.empty and "date" in df.columns:
                # Convertit la colonne texte ("25/08/2026") en vraies dates mathématiques
                dates = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce").dropna()
                if not dates.empty:
                    return dates.max().date()
                    
        # Date de production par défaut
        return datetime.date(2026, 8, 1)

    @staticmethod
    def add_notifications(nouvelles_missions):
        """Ajoute les nouveaux mails trouvés dans l'Excel de cache."""
        if not nouvelles_missions: 
            return
            
        df_new = pd.DataFrame(nouvelles_missions)
        if os.path.exists(NOTIFICATIONS_EXCEL_FILE):
            df = pd.read_excel(NOTIFICATIONS_EXCEL_FILE)
            df = pd.concat([df, df_new], ignore_index=True)
            # Sécurité anti-doublons au cas où IMAP relirait le même jour
            df = df.drop_duplicates(subset=["sujet"], keep='first')
        else:
            df = df_new
            
        df.to_excel(NOTIFICATIONS_EXCEL_FILE, index=False)

    @staticmethod
    def remove_notification(sujet):
        """Retire une mission du cache (quand elle est acceptée ou refusée)."""
        if os.path.exists(NOTIFICATIONS_EXCEL_FILE):
            df = pd.read_excel(NOTIFICATIONS_EXCEL_FILE)
            df = df[df["sujet"] != sujet]
            df.to_excel(NOTIFICATIONS_EXCEL_FILE, index=False)