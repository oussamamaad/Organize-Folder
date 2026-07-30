"""
Organisateur de dossier (ex: Downloads) par type de fichier.

Trie automatiquement les fichiers d'un dossier dans des sous-dossiers
selon leur extension (Images, Documents, Videos, Archives, Audio, etc.).

Installation :
    Aucune dépendance externe requise (uniquement la bibliothèque standard).

Utilisation :
    python organize_folder.py "C:\\Users\\pc\\Downloads"
    python organize_folder.py "C:\\Users\\pc\\Downloads" --dry-run
    python organize_folder.py "C:\\Users\\pc\\Downloads" --watch

Options :
    --dry-run   Affiche ce qui serait fait, sans rien déplacer réellement.
    --watch     Surveille le dossier en continu et organise les nouveaux
                fichiers dès qu'ils apparaissent (Ctrl+C pour arrêter).
"""

import argparse
import logging
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

# --- Configuration : catégories et extensions associées ---
CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".xlsx", ".xls",
                  ".ppt", ".pptx", ".csv"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".iso"},
    "Programs": {".exe", ".msi", ".apk", ".deb", ".dmg"},
    "Code": {".py", ".js", ".html", ".css", ".json", ".java", ".cpp", ".c", ".sh"},
}

OTHER_CATEGORY = "Others"
LOG_FILE = "organize_folder.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def get_category(file_path: Path) -> str:
    """Retourne le nom de la catégorie correspondant à l'extension du fichier."""
    ext = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return OTHER_CATEGORY


def resolve_conflict(destination: Path) -> Path:
    """Si un fichier du même nom existe déjà, ajoute un suffixe numéroté."""
    if not destination.exists():
        return destination

    stem, suffix, parent = destination.stem, destination.suffix, destination.parent
    counter = 1
    new_destination = parent / f"{stem} ({counter}){suffix}"
    while new_destination.exists():
        counter += 1
        new_destination = parent / f"{stem} ({counter}){suffix}"
    return new_destination


def organize_folder(target_dir: Path, dry_run: bool = False) -> int:
    """Organise les fichiers de target_dir en sous-dossiers par catégorie.

    Retourne le nombre de fichiers déplacés (ou qui seraient déplacés en dry-run).
    """
    if not target_dir.is_dir():
        logger.error(f"Le dossier n'existe pas : {target_dir}")
        return 0

    moved_count = 0
    known_folders = set(CATEGORIES.keys()) | {OTHER_CATEGORY}

    for item in target_dir.iterdir():
        # On ignore les dossiers (y compris ceux qu'on a nous-mêmes créés)
        if item.is_dir():
            continue
        # On ignore le fichier de log lui-même
        if item.name == LOG_FILE:
            continue

        category = get_category(item)
        dest_folder = target_dir / category
        destination = resolve_conflict(dest_folder / item.name)

        if dry_run:
            logger.info(f"[DRY-RUN] {item.name} -> {category}/{destination.name}")
        else:
            dest_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
            logger.info(f"Déplacé : {item.name} -> {category}/{destination.name}")

        moved_count += 1

    return moved_count


def watch_folder(target_dir: Path, interval: int = 5):
    """Surveille le dossier en continu et organise les nouveaux fichiers."""
    logger.info(f"Surveillance de {target_dir} démarrée (Ctrl+C pour arrêter).")
    try:
        while True:
            count = organize_folder(target_dir, dry_run=False)
            if count:
                logger.info(f"{count} fichier(s) organisé(s) à {datetime.now():%H:%M:%S}.")
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Surveillance arrêtée.")


def main():
    parser = argparse.ArgumentParser(
        description="Organise automatiquement un dossier par type de fichier."
    )
    parser.add_argument("folder", type=str, help="Chemin du dossier à organiser")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Affiche ce qui serait fait sans rien déplacer réellement"
    )
    parser.add_argument(
        "--watch", action="store_true",
        help="Surveille le dossier en continu et organise les nouveaux fichiers"
    )
    parser.add_argument(
        "--interval", type=int, default=5,
        help="Intervalle (secondes) entre chaque vérification en mode --watch (défaut: 5)"
    )
    args = parser.parse_args()

    target_dir = Path(args.folder).expanduser().resolve()

    if args.watch:
        watch_folder(target_dir, interval=args.interval)
    else:
        count = organize_folder(target_dir, dry_run=args.dry_run)
        mode = "seraient organisés (dry-run)" if args.dry_run else "organisés"
        logger.info(f"Terminé : {count} fichier(s) {mode}.")


if __name__ == "__main__":
    main()
