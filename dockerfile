# Dockerfile
FROM apache/airflow:2.5.1   

USER airflow


COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

