import os

APP_NAME = "MAJ - Manageur d'affaires juridiques"

# Chemin absolu vers l'icône (dossier assets à la racine du projet)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "assets", "app_icon.png")
MISE_A_JOUR_PAYEMENT_ICON_PATH = os.path.join(BASE_DIR, "assets", "update_transaction.png")

# --- DIMENSIONS DE LA FENÊTRE ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# --- CHEMIN DU FICHIER EXCEL ---
EXCEL_FILE = os.path.join(BASE_DIR, "assets", "EXPERTISES JUDICIAIRES.xlsx")
OPJ_EXCEL_FILE = os.path.join(BASE_DIR, "assets", "EXPERTISES JUDICIAIRES- OPJ.xlsx")
JAF_EXCEL_FILE = os.path.join(BASE_DIR, "assets", "EXPERTISES JUDICIAIRES- JAF.xlsx")
JI_EXCEL_FILE = os.path.join(BASE_DIR, "assets", "EXPERTISES JUDICIAIRES- JI.xlsx")

# --- COLONNES EN BACK DES TABLEAUX ---
OPJ_BACK_COLUMNS = [
        "NOM",
        "Planification",
        "Column 13",
        "Propriétaire",
        "CHORUS PRO",
        "periode",
        "montant",
        "État",
        "État 2"
    
]
JAF_BACK_COLUMNS = [
        "NOM",
        "Planification",
        "DATE",
        "date de redaction du rapport",
        "DATE REMISE DES RAPPORT",
        "periode",
        "État",
        "État 2",
        "montant",
]

JI_BACK_COLUMNS = [
        "NOM",
        "periode",
        "Planification",
        "CHORUS PRO",
        "État",
        "État 2",
        "montant"
]

# --- COLONNES AFFICHER DES TABLEAUX (Clé = En backend, Valeur = Nom affiché) ---
OPJ_FRONT_COLUMNS = {
        "NOM": "NOM",
        "periode": "Période de l'affaire",
        "Propriétaire": "Propriétaire",
        "CHORUS PRO": "Réf. CHORUS PRO",
        "Planification": "Planification",
        "État": "État du rapport",
        "État 2": "Statut du paiement",
        "montant": "Montant (€)"
}

JAF_FRONT_COLUMNS = {
        "NOM": "NOM",
        "periode": "Période de l'affaire",
        "Propriétaire": "Propriétaire",
        "Planification": "Planification",
        "date de redaction du rapport": "Date de rédaction",
        "DATE REMISE DES RAPPORT": "Date de remise",
        "État": "État du rapport",
        "État 2": "Statut du paiement",
        "montant": "Montant (€)"
}

JI_FRONT_COLUMNS = {
        "NOM": "NOM",
        "periode": "Période de l'affaire",
        "Propriétaire": "Propriétaire",
        "CHORUS PRO": "Réf. CHORUS PRO",
        "Planification": "Planification",
        "État": "État du rapport",
        "État 2": "Statut du paiement",
        "montant": "Montant (€)"
}

# --- FILTRES ---
OPJ_FILTER_COLUMNS = {
    "periode": "Période",
    "Planification": "Planification Rendez-vous",
    "État": "Statut du rapport",
    "État 2": "Statut du payement",
}
JAF_FILTER_COLUMNS = {
    "periode": "Période",
    "État": "Statut du rapport",
    "État 2": "Statut du payement",
}
JI_FILTER_COLUMNS = {
    "periode": "Période",
    "État": "Statut du rapport",
    "État 2": "Statut du payement",
}

# --- CONFIGURATION DU DASHBOARD ---
# Dictionnaire de tous les indicateurs disponibles (Clé = ID technique, Valeur = Nom affiché)
DASHBOARD_AVAILABLE_PINS = {
    "total_opj": "Total des affaires OPJ",
    "total_jaf": "Total des affaires JAF",
    "total_ji": "Total des affaires JI",
    "attente_paiement": "Dossiers en attente de paiement",
    "montant_total": "Montant total facturé (€)",
    "rapports_a_faire": "Rapports à rédiger",
    "affaires_terminees": "Affaires terminées",
    "chorus_manquants": "Dossiers sans Chorus Pro"
}

# Les 6 clés affichées par défaut au lancement
DASHBOARD_DEFAULT_ACTIVE_PINS = [
    "total_opj", 
    "total_jaf", 
    "total_ji", 
    "attente_paiement", 
    "montant_total", 
    "rapports_a_faire"
]

# --- THÈMES ---
THEME_LIGHT = {
    "bg_main": "#F5F6FA",
    "bg_header": "#FFFFFF",
    "text_main": "#000000",
    "primary_mauve": "#bca0dc",
    "border": "#A4ACAFFF",
    "board_border_background": "#FFFFFF",
    "board_border_color": "#A4ACAFFF",
    "board_background": "#F5F6FA",
}

THEME_DARK = {
    "bg_main": "#1E1E1E",
    "bg_header": "#2D2D2D",
    "text_main": "#FFFFFF",
    "primary_mauve": "#bca0dc",
    "border": "#333333",
    "board_border_background": "#2D2D2D",
    "board_border_color": "#333333",
    "board_background": "#2D2D2D",
}

# --- GÉNÉRATEUR DE STYLE (QSS) ---
def get_stylesheet(theme: dict) -> str:
    """Génère le style global en fonction du dictionnaire de thème fourni."""
    return f"""
        QMainWindow {{
            background-color: {theme['bg_main']};
        }}
        QWidget {{
            color: {theme['text_main']};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }}
        
        /* HEADER */
        #header_frame {{
            background-color: {theme['bg_header']};
            border-bottom: 1px solid {theme['border']};
        }}
        
        /* --- PARTIE HAUTE DU HEADER --- */
        #top_header_widget {{
        }}
        
        /* --- ONGLETS DU HEADER --- */
        #nav_button {{
            border: none; border-radius: 0px; background-color: transparent;
            font-size: 15px; font-weight: bold; color: {theme['text_main']};
            border-bottom: 3px solid transparent; /* Bordure invisible par défaut */
            border: 1px solid {theme['border']};
        }}
        #nav_button:hover {{
            color: {theme['primary_mauve']};
            border-bottom: 3px solid {theme['primary_mauve']}; /* Soulignement mauve au survol */
            background-color: transparent;
        }}
        #nav_button:checked {{
            color: {theme['text_main']};
            border-bottom: 3px solid {theme['primary_mauve']};
            background-color: {theme['primary_mauve']};
        }}
        
        /* --- STYLE DU TABLEAU --- */
        #board_ext_frame {{
            background-color: {theme['board_border_background']};
            border: 1px solid {theme['board_border_color']};
            border-radius: 10px;
        }}
        #board_int_frame {{
            background-color: {theme['board_background']};
            border: 1px solid {theme['board_border_color']};
            border-radius: 10px;
        }}
        
        /* --- STYLE FILTRE ET TRI --- */
        #filter_frame {{
            background-color: {theme['bg_header']};
            border: 1px solid {theme['border']};
        }}
        #tri_frame {{
            background-color: {theme['bg_header']};
            border: 1px solid {theme['border']};
            border-left: none;
        }}
        
        /* --- STYLE DES CARTES --- */
        #card_opj, #card_jaf, #card_ji {{
            background-color: {theme['board_background']};
            border: 1px solid {theme['board_border_color']};
            border-radius: 8px;
        }}
        
        #card_opj:hover, #card_jaf:hover, #card_ji:hover {{
            background-color: {theme['primary_mauve']};
            color: {theme['text_main']};
            border: 1px solid {theme['primary_mauve']};
        }}
        
        /* --- STYLE DES TEXTES A L'INTERIEUR DES CARTES --- */
        
        #card_label_normal {{
            border: none;
            font-size: 14px;
            color: {theme['text_main']};
        }}
        
        #card_label_nom {{
            border: none;
            font-size: 16px;
            color: {theme['text_main']};
        }}
        
        /* --- STYLE DES BOUTONS DE TRI --- */
        #sort_button {{
            background-color: {theme['bg_header']};
            border: 1px solid {theme['border']};
            border-radius: 15px;
            padding: 5px 10px;
            font-size: 13px;
            color: {theme['text_main']};
        }}
        #sort_button:hover {{
            border: 1px solid {theme['primary_mauve']};
        }}
        #sort_button:checked {{
            background-color: {theme['primary_mauve']};
            color: {theme['text_main']};
            border: 1px solid {theme['primary_mauve']};
            font-weight: bold;
        }}
        
        /* --- STYLE DES COMBOBOX (FILTRES) --- */
        QComboBox {{
            background-color: {theme['bg_main']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
            padding: 5px;
            color: {theme['text_main']};
            min-height: 25px;
            font-size: 14px;
        }}
        
        QComboBox QAbstractItemView {{
            font-size: 14px;
            background-color: {theme['board_background']};
            color: {theme['text_main']};
            selection-background-color: {theme['primary_mauve']};
            selection-color: {theme['text_main']};
            outline: none;
        }}
        
        /* --- STYLE DU BOUTON FLOTTANT (MISE A JOUR) --- */
        #fab_update {{
            border-radius: 35px;
            border: none;
        }}
        #fab_update:hover {{
        }}
        #fab_update:pressed {{
        }}
        
        /* --- STYLE DES CARTES DU DASHBOARD --- */
        #card_dashboard {{
            background-color: {theme['board_background']};
            border: 2px solid {theme['primary_mauve']};
            border-radius: 10px;
        }}
        #card_dashboard_header {{
            background-color: {theme['primary_mauve']};
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }}
        #card_dashboard_title {{
            color: {theme['text_main']};
            font-size: 14px;
            font-weight: bold;
        }}
        #card_dashboard_value {{
            color: {theme['primary_mauve']};
            font-size: 32px;
            font-weight: bold;
        }}
    """