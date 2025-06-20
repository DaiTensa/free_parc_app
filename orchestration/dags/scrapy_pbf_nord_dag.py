"""
DAG pour l'exécution automatique du scraper PBF Nord-Pas-de-Calais.
Ce DAG récupère les données géospatiales depuis Geofabrik et les stocke au format JSON.
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import json
import glob

# Configuration des arguments par défaut
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["dai.tensaout@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def check_latest_file(**kwargs):
    """Vérifie si le fichier latest existe et contient des données valides"""
    latest_file = "/usr/local/airflow/data/pbf_nord_pas_de_calais_latest.json"
    
    if not os.path.exists(latest_file):
        raise FileNotFoundError(f"Le fichier {latest_file} n'a pas été créé")
    
    try:
        with open(latest_file, 'r') as f:
            data = json.load(f)
            if not data:
                raise ValueError(f"Le fichier {latest_file} ne contient pas de données valides")
            print(f"Scraping réussi : {len(data)} éléments récupérés")
    except json.JSONDecodeError:
        raise ValueError(f"Le fichier {latest_file} n'est pas un JSON valide")

# Création du DAG
with DAG(
    dag_id="scrapy_pbf_nord_dag",
    default_args=default_args,
    description="Récupération des données géospatiales du Nord-Pas-de-Calais depuis Geofabrik",
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 3 * * *",  # Exécution quotidienne à 3h du matin
    catchup=False,
    tags=['scraper', 'geospatial', 'nord-pas-de-calais'],
) as dag:

    # Tâche d'exécution du scraper et gestion des fichiers en une seule étape
    run_scraper = BashOperator(
        task_id="run_scraper",
        bash_command="""
            # Créer le dossier data si nécessaire
            mkdir -p /usr/local/airflow/data
            
            # Définir le nom du fichier avec la date du jour
            DATE=$(date +%Y%m%d)
            BASE_FILE="/usr/local/airflow/data/pbf_nord_pas_de_calais_${DATE}.json"
            
            # Vérifier si le fichier du jour existe déjà
            if [ -f "$BASE_FILE" ]; then
                # Si oui, créer un fichier avec horodatage
                TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                OUTPUT_FILE="/usr/local/airflow/data/pbf_nord_pas_de_calais_${TIMESTAMP}.json"
            else
                # Sinon, utiliser le fichier avec juste la date
                OUTPUT_FILE="$BASE_FILE"
            fi
            
            # Exécuter le scraper
            source /usr/local/airflow/airflow_venv/bin/activate
            cd /usr/local/airflow/scraper/pbfcrwal
            scrapy crawl pbf_nord_pas_de_calais -O $OUTPUT_FILE
            
            # Créer ou mettre à jour le fichier latest
            cp $OUTPUT_FILE /usr/local/airflow/data/pbf_nord_pas_de_calais_latest.json
            
            echo "Données enregistrées dans $OUTPUT_FILE et copiées dans le fichier latest"
        """
    )
    
    # Tâche de vérification du résultat
    check_result = PythonOperator(
        task_id="check_result",
        python_callable=check_latest_file
    )

    # Tâche pour traitement des données
    process_data = BashOperator(
        task_id="process_data",
        bash_command="""
            source /usr/local/airflow/airflow_venv/bin/activate
            cd /usr/local/airflow/scraper
            
            # Utiliser le fichier latest pour le traitement
            echo "Traitement des données du fichier latest..."
            python -c "print('Traitement des données en cours...')"
            
            # Vous pouvez ajouter votre script de traitement ici
            echo "Traitement terminé avec succès"
        """
    )

    # Définition du workflow
    run_scraper >> check_result >> process_data