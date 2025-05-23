import os
import sys
import requests
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional

ENV_PROJECT_ROOT = "CORPUS_TOOL_ROOT"
ENV_RAW_DATA_DIR = "RAW_DATA_DIR"

def get_project_root() -> Path:
    """Trouver la racine de l'Outils-de-traitement-de-corpus"""
    current_dir = Path(__file__).absolute().parent
    while current_dir != current_dir.parent:  # Arrêter à la racine
        if current_dir.name == "Outils-de-traitement-de-corpus":
            return current_dir
        current_dir = current_dir.parent
    raise FileNotFoundError("La racine n'a pas été trouvée")

def get_data_dir() -> Path:
    """Obtenir la direction pour enregistrer les données"""
    if raw_dir := os.getenv(ENV_RAW_DATA_DIR):
        return Path(raw_dir)
    
    # Outils-de-traitement-de-corpus/data/raw
    return get_project_root() / "data" / "raw"

def fetch_and_save(url: str) -> Optional[Path]:
    try:
        save_dir = get_data_dir()
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Le nom du fichier
        parsed = urlparse(url)
        domain = parsed.netloc.replace(".", "_")
        path = "_".join(filter(None, parsed.path.split("/"))) or "index"
        filename = f"{domain}_{path}.html"
        save_path = save_dir / filename
        
        # Récupérer les données
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=(5, 15)
        )
        response.raise_for_status()
        
        
        # enregistrer le fichier
        save_path.write_text(response.text, encoding='utf-8')
        print(f"Le fichier enregistré dans: {save_path.relative_to(get_project_root())}")
        return save_path
        
    except Exception as e:
        print(f"Erreur：{type(e).__name__}: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Entrez URL du site web")
    args = parser.parse_args()
    
    saved_path = fetch_and_save(args.url)
    sys.exit(0 if saved_path else 1)