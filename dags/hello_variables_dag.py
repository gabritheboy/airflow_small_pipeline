from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import boto3



BUCKET = "mock-bucket"
KEY = "data.csv"

def create_mock_s3():
    """Crea bucket S3 e CSV finto con Moto"""
    with mock_s3():
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=BUCKET)
        csv_data = "id,speed\n1,50\n2,60\n3,70"
        s3.put_object(Bucket=BUCKET, Key=KEY, Body=csv_data)
        print(f"[Extract] File caricato in bucket {BUCKET}")


# Funzioni Python per i task
def task1(ti, **kwargs):
    x = 5
    print(f"[Task1] Valore generato: {x}")
    
    # Passiamo il valore al task successivo usando XCom
    ti.xcom_push(key='valore', value=x)

def task2(ti, **kwargs):
    # Recuperiamo il valore dal task1
    x = ti.xcom_pull(key='valore', task_ids='task1')
    y = x + 10
    
    print(f"[Task2] Valore ricevuto: {x}, dopo trasformazione: {y}")
    
    # Possiamo anche passarlo avanti
    ti.xcom_push(key='valore2', value=y)

def task3(ti, **kwargs):
    
    y = ti.xcom_pull(key='valore2', task_ids='task2')
    print(f"[Task3] Valore finale ricevuto: {y}")

# Definizione DAG
with DAG(
    'hello_variables_dag',
    start_date=days_ago(0),
    schedule_interval=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id='task1',
        python_callable=task1
    )

    t2 = PythonOperator(
        task_id='task2',
        python_callable=task2
    )

    t3 = PythonOperator(
        task_id='task3',
        python_callable=task3
    )

    # Definiamo l’ordine di esecuzione
    t1 >> t2 >> t3
