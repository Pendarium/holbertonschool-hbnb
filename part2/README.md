# HBnB Project

## Structure du projet

- `app/` : Code principal de l’application
  - `api/` : Points de terminaison de l’API (versionnés par `v1/`)
  - `models/` : Classes métier (User, Place, Review, Amenity)
  - `services/` : Logique de coordination (modèle Façade)
  - `persistence/` : Gestion du stockage (référentiel en mémoire)
- `run.py` : Point d’entrée pour exécuter l’application Flask
- `config.py` : Configuration des paramètres de l’application
- `requirements.txt` : Liste des packages Python nécessaires
- `README.md` : Documentation du projet

## Installation

1. Créez un environnement virtuel (optionnel mais recommandé) :

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
