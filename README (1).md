# Organize Folder

Script Python qui trie automatiquement les fichiers d'un dossier (ex:
Downloads) dans des sous-dossiers selon leur type : Images, Documents,
Videos, Audio, Archives, Programs, Code, et Others pour tout le reste.

## Fonctionnalités

- Tri automatique par extension de fichier
- Mode `--dry-run` : simule l'organisation sans rien déplacer
- Mode `--watch` : surveille le dossier en continu et organise les
  nouveaux fichiers dès qu'ils apparaissent
- Gestion des conflits de noms (ajoute `(1)`, `(2)`... si un fichier du
  même nom existe déjà)
- Journal des actions (`organize_folder.log`)

## Prérequis

- Python 3.8+
- Aucune dépendance externe (bibliothèque standard uniquement)

## Installation

```bash
git clone <votre-repo>
cd organize-folder
```

Rien d'autre à installer.

## Utilisation

**Tester sans rien déplacer (recommandé la première fois) :**

```bash
python organize_folder.py "C:\Users\pc\Downloads" --dry-run
```

**Organiser réellement le dossier :**

```bash
python organize_folder.py "C:\Users\pc\Downloads"
```

**Surveiller le dossier en continu** (organise chaque nouveau fichier
automatiquement) :

```bash
python organize_folder.py "C:\Users\pc\Downloads" --watch
```

Arrêter la surveillance avec `Ctrl+C`.

## Options

| Option | Rôle | Défaut |
| --- | --- | --- |
| `folder` | Chemin du dossier à organiser (obligatoire) | — |
| `--dry-run` | Simule l'organisation sans déplacer les fichiers | désactivé |
| `--watch` | Surveille le dossier en continu | désactivé |
| `--interval` | Intervalle (secondes) entre chaque vérification en mode `--watch` | `5` |

## Catégories et extensions

Modifiables directement dans `organize_folder.py`, dans le dictionnaire
`CATEGORIES` en haut du fichier :

```python
CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ...},
    "Documents": {".pdf", ".doc", ".docx", ...},
    "Videos": {".mp4", ".mkv", ...},
    "Audio": {".mp3", ".wav", ...},
    "Archives": {".zip", ".rar", ...},
    "Programs": {".exe", ".msi", ...},
    "Code": {".py", ".js", ".html", ...},
}
```

Tout fichier dont l'extension n'est dans aucune catégorie va dans
`Others`. Pour ajouter une catégorie, il suffit d'ajouter une nouvelle
entrée au dictionnaire.

## Structure du projet

```text
.
├── organize_folder.py       # script principal
├── organize_folder.log      # généré automatiquement à l'exécution
└── README.md
```

## Problèmes courants

- **"Le dossier n'existe pas"** : vérifiez le chemin fourni, surtout les
  antislashs sous Windows (mettez le chemin entre guillemets).
- **Fichiers en cours de téléchargement déplacés par erreur** : en mode
  `--watch`, évitez un `--interval` trop court si vous téléchargez de gros
  fichiers, pour laisser le temps au téléchargement de se terminer.
- **Fichiers non triés comme attendu** : vérifiez que leur extension est
  bien dans une des catégories de `CATEGORIES` ; sinon ils atterrissent
  dans `Others`.

## Améliorations possibles

- Tri par date au lieu de / en plus du type de fichier
- Exclusion de certains fichiers/dossiers via une liste d'ignorance
- Interface graphique simple pour choisir le dossier et les catégories
- Notification système quand des fichiers sont organisés

## Licence

Projet personnel — libre d'utilisation et de modification.
