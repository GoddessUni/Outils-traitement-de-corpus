import sys
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Optional
import re

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    
    # Supprimer les étiquettes inutiles
    for tag in soup(['script', 'style', 'nav', 'footer', 'table', 'iframe', 'svg']):
        tag.decompose()
    
    main_content = soup.find('div', id='bodyContent') or soup.find('main') or soup.body
    
    text = ' '.join(main_content.stripped_strings) if main_content else ''
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[\d+\]', '', text)
    return text.strip()

def process_file(input_path: Path) -> Optional[Path]:
    try:
        html = input_path.read_text(encoding='utf-8')
        cleaned_text = clean_html(html)
        
        output_path = Path.cwd() / f"{input_path.stem}_cleaned.txt"
        output_path.write_text(cleaned_text, encoding='utf-8')
        
        print(f"fichier nettoyé -> {output_path.name}")
        return output_path

    except Exception as e:
        print(f"Erreur de traitement {input_path.name}: {type(e).__name__} - {e}", file=sys.stderr)
        return None

def batch_process() -> int:
    # Traiter les fichiers html
    raw_dir = Path.cwd()
    html_files = list(raw_dir.glob("*.html"))
    
    if not html_files:
        print("Aucun fichier .html trouvé dans le répertoire courant.")
        return 1

    success_count = 0
    for html_file in html_files:
        if process_file(html_file):
            success_count += 1

    print(f"\nFin de traitement: {success_count} succès, {len(html_files) - success_count} échoués")
    return 0 if success_count > 0 else 1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Nettoyer HTML vers texte")
    parser.add_argument("--input", help="Fichier HTML individuel à traiter")
    args = parser.parse_args()

    if args.input:
        sys.exit(0 if process_file(Path(args.input)) else 1)
    else:
        sys.exit(batch_process())
