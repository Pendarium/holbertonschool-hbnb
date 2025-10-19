# Holberton BnB (HBNB) – Part 2

## Description
Ce projet implémente le backend d’une application de location de logements de type Airbnb.  
Il utilise **Flask-RESTx** pour l’API REST et un **système de persistance en mémoire**.  
Toutes les entités sont connectées entre elles et des validations sont appliquées pour garantir l’intégrité des données.

---

## Structure du Projet

part2/
├── app/ 
│ ├── init.py
│ ├── models/
│ │ ├── base_model.py
│ │ ├── user.py
│ │ ├── place.py
│ │ ├── amenity.py
│ │ └── review.py
│ ├── services/
│ │ └── facade.py
│ └── persistence/
│ ├── repository.py
│ └── ...
├── tests/
│ ├── test_users.py
│ ├── test_places.py
│ ├── test_amenities.py
│ └── test_reviews.py
└── run.py

---

## Entités et Validations

### User
- `first_name`, `last_name`, `email` ne doivent pas être vides.
- `email` doit être dans un format valide.
- Relation avec `Place` et `Review` (un utilisateur peut avoir plusieurs places et reviews).

### Place
- `title` ne doit pas être vide.
- `price` doit être positif.
- `latitude` entre -90 et 90.
- `longitude` entre -180 et 180.
- Relations : `owner` (User) et `amenities` (liste d’Amenity).

### Amenity
- `name` ne doit pas être vide.
- Relation avec `Place` (un amenity peut appartenir à plusieurs places).

### Review
- `text` ne doit pas être vide.
- `user_id` et `place_id` doivent pointer vers des entités existantes.

---

## API REST

Les endpoints sont documentés via **Swagger**.  
Pour accéder à la documentation, lancer le serveur et visiter :


### Principaux Endpoints

| Ressource | Méthode | Description |
|-----------|---------|------------|
| /users/ | POST | Créer un utilisateur |
| /users/ | GET | Lister tous les utilisateurs |
| /users/<user_id> | GET | Récupérer un utilisateur par ID |
| /users/<user_id> | PUT | Mettre à jour un utilisateur |
| /places/ | POST | Créer un lieu |
| /places/ | GET | Lister tous les lieux |
| /places/<place_id> | GET | Récupérer un lieu par ID |
| /places/<place_id> | PUT | Mettre à jour un lieu |
| /amenities/ | POST | Créer un amenity |
| /amenities/ | GET | Lister tous les amenities |
| /amenities/<amenity_id> | GET | Récupérer un amenity par ID |
| /amenities/<amenity_id> | PUT | Mettre à jour un amenity |
| /reviews/ | POST | Créer un review |
| /reviews/ | GET | Lister tous les reviews |
| /reviews/<review_id> | GET | Récupérer un review par ID |
| /reviews/<review_id> | PUT | Mettre à jour un review |

---

## Lancer le Projet

1. Créer un environnement virtuel et installer les dépendances :

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

2. Lancer le serveur :
    ```bash
    python3 run.py

3. Tester les endpoints via Swagger ou cURL.

### Tests Unitaires

#### Les tests sont dans le dossier tests/. Pour exécuter tous les tests :
    ```bash
    python3 -m unittest discover -s tests -p "test_*.py"
### Tous les tests couvrent :
1. Création valide et invalide de chaque entité.
2. Validations de champs obligatoires et formats.
3. Relations entre entités.
4. Mise à jour des entités et gestion des erreurs.

# CREER PAR
SORLI Thomas