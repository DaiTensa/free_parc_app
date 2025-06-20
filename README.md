# FreeParcApp

poetry init

poetry install --no-root

poetry add fastapi uvicorn pydantic sqlalchemy asyncpg python-dotenv

eval $(poetry env activate) 

poetry env info

Virtualenv
Python:         3.12.3
Implementation: CPython
Path:           /mnt/c/Users/daite/Documents/Python_Projects/free_parc_app/.venv
Executable:     /mnt/c/Users/daite/Documents/Python_Projects/free_parc_app/.venv/bin/python
Valid:          True

Base
Platform:   linux
OS:         posix
Python:     3.12.3
Path:       /usr
Executable: /usr/bin/python3.12

poetry env info --path
/mnt/c/Users/daite/Documents/Python_Projects/free_parc_app/.venv

poetry env info --executable
/mnt/c/Users/daite/Documents/Python_Projects/free_parc_app/.venv/bin/python


poetry env remove /full/path/to/python


Streamlit 
poetry run streamlit run app.py


# base de donnée
sudo apt update

installer postgresql

 sudo apt install postgresql postgresql-contrib

 vérifier si postgre est installé 
 sudo systemctl status postgresql


 accéder à ppostgre en tant que utilisateur postgres
 sudo -i -u postgres

 lancer la console psql
psql

créer un utilisateur 
CREATE USER user_test WITH PASSWORD 'pass1234';

garantir les privi
GRANT ALL PRIVILEGES ON DATABASE db_test TO user_test;
GRANT USAGE ON SCHEMA public TO user_test;
GRANT CREATE ON SCHEMA public TO user_test;

GRANT CONNECT ON DATABASE db_test TO user_test;


Installer les dépendances nécessaires pour la compilation de psycopg2 
sudo apt-get update
sudo apt-get install -y libpq-dev build-essential


installer psycopg2
poetry add psycopg2

# changement du non de mon repo remote

Conséquences en local -> remote n'est plus valide
Solution :
- vérifier l'url actuelle 
git remote -v

origin  https://github.com/ancien-nom-repo.git (fetch)
origin  https://github.com/ancien-nom-repo.git (push)


- changer l'url du remote après avoir renommer le repo

git remote set-url origin https://github.com/nouveau-nom-repo.git

git branch -r Lists all the remote branches

