import os

APP_NAME = "MAJ - Manageur d'affaires juridiques"

# Chemin absolu vers l'icône (dossier assets à la racine du projet)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "assets", "app_icon.png")

# --- DIMENSIONS DE LA FENÊTRE ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# --- THÈMES ---
THEME_LIGHT = {
    "bg_main": "#FFFFFF",
    "text_main": "#2D3436",
    "primary_mauve": "#bca0dc",
    "border": "#DFE6E9",
}

THEME_DARK = {
    "bg_main": "#1E1E1E",
    "text_main": "#FFFFFF",
    "primary_mauve": "#bca0dc", # On peut garder le même mauve ou l'adapter
    "border": "#333333",
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
    """