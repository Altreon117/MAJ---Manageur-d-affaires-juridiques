import os

APP_NAME = "MAJ - Manageur d'affaires juridiques"

# Chemin absolu vers l'icône (dossier assets à la racine du projet)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "assets", "app_icon.png")

# --- DIMENSIONS DE LA FENÊTRE ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# --- CHEMIN DU FICHIER EXCEL ---
EXCEL_FILE = os.path.join(BASE_DIR, "assets", "EXPERTISES JUDICIAIRES.xlsx")
OPJ_EXCEL_FILE = os.path.join(BASE_DIR, "assets", "EXPERTISES JUDICIAIRES- OPJ.xlsx")
JAF_EXCEL_FILE = os.path.join(BASE_DIR, "assets", "EXPERTISES JUDICIAIRES- JAF.xlsx")

# --- COLONNES EN BACK DES TABLEAUX ---
OPJ_BACK_COLUMNS = [
        "NOM",
        "Planification",
        "Propriétaire",
        "CHORUS PRO",
        "periode",
        "montant"
    
]
JAF_BACK_COLUMNS = [
        "NOM"
]

# --- COLONNES AFFICHER DES TABLEAUX ---
OPJ_FRONT_COLUMNS = [
        "NOM",
        "Planification",
        "Propriétaire",
        "CHORUS PRO",
        "periode",
        "montant"
]
JAF_FRONT_COLUMNS = [
        "NOM"
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
    "board_background": "#FFFFFF",
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
        #card_opj, #card_jaf {{
            background-color: {theme['board_background']};
            border: 1px solid {theme['board_border_color']};
            border-radius: 8px;
        }}
        
        #card_opj:hover, #card_jaf:hover {{
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
            color: #1877F2; /* Bleu de mise en évidence */
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
    """