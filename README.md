# Free Park App

[![Python](https://img.shields.io/badge/Python-3.12.3-blue.svg)](https://www.python.org/)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)

[![Streamlit](https://img.shields.io/badge/Streamlit-1.44.0-red.svg)](https://streamlit.io/)

[![Airflow](https://img.shields.io/badge/Airflow-2.7.0-orange.svg)](https://airflow.apache.org/)

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue.svg)](https://www.postgresql.org/)


## 📋 Table des Matières

- Présentation du Projet
- Architecture du Système
- Configuration et Installation
- Composants Principaux
- API Endpoints
- Workflow de Développement
- Déploiement
- Données Géospatiales
- Auteurs

## Présentation du Projet

FreeParKApp est une plateforme  permettant le partage de places de parking entre particuliers. L'application permet aux utilisateurs de mettre à disposition leurs places de parking inutilisées et de réserver des places disponibles à proximité.

### Fonctionnalités principales:
- Création de compte et authentification des utilisateurs
- Publication de places de parking disponibles avec localisation GPS
- Recherche et réservation de places de parking
- Gestion des réservations en cours
- Collecte automatisée de données géospatiales pour améliorer le service

## Architecture du Système
Le projet est organisé en plusieurs composants interconnectés:

```sh
FreeParcApp/
├── backend/           # API FastAPI et logique métier
├── frontend/          # Interface utilisateur Streamlit
├── data-lake/         # Traitement des données collectées
├── scraper/           # Collecte de données géospatiales
├── orchestration/     # Automatisation des workflows avec Airflow
├── docs/              # Documentation
└── tests/             # Tests unitaires et d'intégration
```

## Configuration et Installation

### Prérequis
- Python 3.12.3+

- PostgreSQL

- Docker et Docker Compose (pour Airflow)

### Installation

1. **Cloner le dépôt**

 ```sh
 git clone https://github.com/votre-username/free-parc-app.git
 cd free-parc-app
 ```
2. **Configurer l'environnement Python avec Poetry**

 ```sh
 poetry install --no-root
 ```

3. **Configurer la base de données PostgreSQL**

 ```sh
 sudo apt update
 sudo apt install postgresql postgresql-contrib
 sudo systemctl status postgresql
 # Accéder à PostgreSQL
 sudo -i -u postgres
 psql
 # Créer un utilisateur et une base de données
 CREATE USER user_test WITH PASSWORD 'pass1234';
 CREATE DATABASE db_test;
 GRANT ALL PRIVILEGES ON DATABASE db_test TO user_test;
 GRANT USAGE ON SCHEMA public TO user_test;
 GRANT CREATE ON SCHEMA public TO user_test;
 GRANT CONNECT ON DATABASE db_test TO user_test;
 ```

4. **Configurer les variables d'environnement**

 ```sh
 # Créer un fichier .env à la racine du projet
 DBHOST=localhost
 DBNAME=db_test
 DBUSER=user_test
 PASSWORD=pass1234
 SECRET_KEY=votre_clé_secrète
 ALGORITHM=HS256
 ACCESS_TOKEN_EXPIRE_MINUTES=30
 ```
 
## Composants Principaux

### Backend (FastAPI)
Le backend est construit avec FastAPI et fournit l'API REST pour toutes les fonctionnalités de l'application.

**Lancement du serveur backend:**

```sh
cd backend
uvicorn app.main:app --reload
```

Le serveur démarre sur http://127.0.0.1:8000 
avec la documentation API disponible sur http://127.0.0.1:8000/docs

### Frontend (Streamlit)
L'interface utilisateur est développée avec Streamlit pour une expérience interactive.
**Lancement de l'interface utilisateur:**

```sh
cd frontend
streamlit run app.py
```

L'interface sera accessible sur http://localhost:8501

### Scraper (Scrapy)
Un scraper pour collecter des données géospatiales de la région Nord-Pas-de-Calais depuis Geofabrik.

**Exécution manuelle du scraper:**

```sh
cd scraper/pbfcrwal
python scrap_process.py
```

### Orchestration (Airflow)
Airflow est utilisé pour automatiser l'exécution du scraper et le traitement des données.

**Lancement d'Airflow:**

```sh
./run_astro.sh
```

L'interface Airflow sera accessible sur http://localhost:8080

## API Endpoints
### Authentification

| Méthode | Endpoint      | Description                         |
| ------- | ------------- | ----------------------------------- |
| POST    | `/auth/login` | Connexion et obtention du token JWT |

### Utilisateurs

| Méthode | Endpoint     | Description                      |
| ------- | ------------ | -------------------------------- |
| POST    | `/users/new` | Création d'un nouvel utilisateur |
| GET     | `/users/all` | Liste de tous les utilisateurs   |

### Places de Parking

| Méthode | Endpoint                  | Description                              |
| ------- | ------------------------- | ---------------------------------------- |
| POST    | `/parkingspots/create`    | Création d'une nouvelle place de parking |
| GET     | `/parkingspots/available` | Liste des places disponibles             |

### Réservations

| Méthode | Endpoint                             | Description                    |
| ------- | ------------------------------------ | ------------------------------ |
| POST    | `/reservations/`                     | Création d'une réservation     |
| PUT     | `/reservations/{reservation_id}/end` | Terminer une réservation       |
| GET     | `/reservations/available`            | Liste des réservations actives |

## Workflow de Développement

1. **Environnement virtuel**

 ```sh
 poetry shell
 ```

  
2. **Structure de la base de données**

   - Le modèle de données est défini dans models.py

   - Les schémas Pydantic sont dans schemas.py

2. **Tests**

 ```sh
 pytest tests/
 ```

## Déploiement

### Configuration de l'environnement de production

1. **Variables d'environnement**

Assurez-vous de configurer les variables d'environnement correctement pour la production.

2. **Base de données**
Utilisez une instance PostgreSQL sécurisée pour la production.

3. **Serveur Web**

Déployez l'API FastAPI derrière un proxy comme Nginx avec Gunicorn.

## Données Géospatiales

Le projet utilise des données OpenStreetMap pour la région Nord-Pas-de-Calais, récupérées automatiquement via un scraper Scrapy qui collecte les fichiers .osm.pbf depuis Geofabrik.

Ces données sont utilisées pour enrichir l'expérience utilisateur en fournissant des informations contextuelles sur les emplacements de parking.

## Auteur
- **DaiTensa** - [GitHub](https://github.com/DaiTensa)
