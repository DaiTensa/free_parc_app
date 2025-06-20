FROM quay.io/astronomer/astro-runtime:12.8.0

ENV VENV_PATH="/usr/local/airflow/airflow_venv"
ENV PATH="$VENV_PATH/bin:$PATH"

COPY ./requirements.txt /tmp/requirements.txt

RUN python -m venv $VENV_PATH && \
    source $VENV_PATH/bin/activate && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Copie le scraper dans le conteneur
COPY scraper /usr/local/airflow/scraper

