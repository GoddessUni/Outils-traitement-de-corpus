import sys
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Optional
import re

def get_project_root() -> Path:
    """Trouver la racine"""
    current_dir = Path(__file__).absolute().parent
    while current_dir != current_dir.parent:
        if current_dir.name == "Outils-de-traitement-de-corpus":
            return current_dir
        current_dir = current_dir.parent
    raise FileNotFoundError("La racine n'a pas été trouvée")

def get_clean_dir() -> Path:
    return get_project_root() / "data" / "clean"

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    
    # Supprimer les étiquettes
    for tag in soup(['script', 'style', 'nav', 'footer', 'table', 'iframe', 'svg']):
        tag.decompose()
    
    main_content = soup.find('div', id='bodyContent') or soup.find('main') or soup.body
    
    # Obtenir le fichier txt
    text = ' '.join(main_content.stripped_strings)
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'\[\d+\]', '', text) # Supprimer l'étiquette de citation
    return text.strip()

def process_file(input_path: Path) -> Optional[Path]:
    try:
        # Lire le fichier initial
        html = input_path.read_text(encoding='utf-8')
        
        # nettoyage
        cleaned_text = clean_html(html)
        
        clean_dir = get_clean_dir()
        clean_dir.mkdir(parents=True, exist_ok=True)
        output_path = clean_dir / f"{input_path.stem}_cleaned.txt"
        
        # Enregistrer le fichier nettoyé
        output_path.write_text(cleaned_text, encoding='utf-8')
        print(f"fichier nettoyé -> {output_path.relative_to(get_project_root())}")
        return output_path
        
    except Exception as e:
        print(f"Erreur de traitement {input_path.name}: {type(e).__name__} - {e}", file=sys.stderr)
        return None

def batch_process(raw_dir: Optional[Path] = None) -> int:
    #Traiter tous les fichier html
    raw_dir = raw_dir or (get_project_root() / "data" / "raw")
    if not raw_dir.exists():
        print(f"La direction n'existe pas: {raw_dir}", file=sys.stderr)
        return 1
    
    success_count = 0
    for html_file in raw_dir.glob("*.html"):
        if process_file(html_file):
            success_count += 1
    
    print(f"\n Fin de traitement: {success_count} avec succès，{len(list(raw_dir.glob('*.html'))) - success_count} échoué")
    return 0 if success_count > 0 else 1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="nettoyage")
    parser.add_argument("--input", help="Entrez la direction du fichier")
    args = parser.parse_args()
    
    if args.input:
        sys.exit(0 if process_file(Path(args.input)) else 1)
    else:
        sys.exit(batch_process())