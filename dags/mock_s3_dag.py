from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from moto import mock_s3, mock_lambda
import boto3
from io import StringIO
import pandas as pd
import json

BUCKET_INPUT = "mock-bucket"
BUCKET_OUTPUT = "mock-bucket-bronze"
KEY_INPUT = "data.csv"
KEY_OUTPUT = "bronze/data.csv"


@mock_s3
def create_mock_s3():
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=BUCKET_INPUT)
    s3.create_bucket(Bucket=BUCKET_OUTPUT)
    csv_data = "id,speed\n1,50\n2,60\n3,70"
    s3.put_object(Bucket=BUCKET_INPUT, Key=KEY_INPUT, Body=csv_data)
    print(f"[Extract] File CSV caricato in {BUCKET_INPUT}/{KEY_INPUT}")


@mock_lambda
def trigger_lambda_mock(ti):
    client = boto3.client("lambda", region_name="us-east-1")
    payload = {
        "my_name": ["Airflow","Windows","Linux"],
        "my_age": [ 25, 30, 35 ],
    }

    values_to_go =ti.xcom_push(key="lambda_response", value=payload)
    print(f"[Lambda] Invoked values:{payload}")
    return payload

@mock_s3
def run_databricks_notebook_mock(ti):
    my_json = ti.xcom_pull(key="lambda_response", task_ids="trigger_lambda_mock")
    s3 = boto3.client("s3", region_name="us-east-1")
    df = pd.DataFrame(my_json)
    print(f" Payload Lambda ricevuto: {df}")
    
    df["new column"] = df.my_name.apply(lambda x: len(x)) * df.my_age.map(lambda x: x if (x % 2 == 0) else 3)
    out_buffer = StringIO()
    df.to_csv(out_buffer, index=False)
    s3.create_bucket(Bucket=BUCKET_OUTPUT)
    s3.put_object(Bucket=BUCKET_OUTPUT, Key=KEY_OUTPUT, Body=out_buffer.getvalue())
    print(f"[Databricks Job] File salvato su {BUCKET_OUTPUT}/{KEY_OUTPUT}")
    print(f" Payload Lambda ou: {df}")
    

with DAG(
    "etl_with_lambda_mock",
    start_date=datetime(2025, 9, 27),
    schedule_interval=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="create_mock_s3",
        python_callable=create_mock_s3,
    )

    t2 = PythonOperator(
        task_id="trigger_lambda_mock",
        python_callable=trigger_lambda_mock,
    )

    t3 = PythonOperator(
        task_id="run_databricks_notebook",
        python_callable=run_databricks_notebook_mock,
    )

    t1 >> t2 >> t3