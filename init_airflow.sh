#!/bin/bash
# inizializza il database
airflow db init

# crea utente admin se non esiste
airflow users create \
    --username airflow \
    --password airflow \
    --firstname Airflow \
    --lastname Admin \
    --role Admin \
    --email airflow@example.com || true

# avvia scheduler e webserver
airflow scheduler & airflow webserver
