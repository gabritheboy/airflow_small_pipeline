from datetime import datetime
from io import StringIO
import json

BUCKET_INPUT = "mock-bucket"
BUCKET_OUTPUT = "mock-bucket-bronze"
KEY_INPUT = "data.csv"
KEY_OUTPUT = "bronze/data.csv"




def trigger_lambda_mock():
    payload = {
        "my_name": ["Airflow","Windows","Linux"],
        "my_age": [ 25, 30, 35 ],
    }

    print(f"[Lambda] Invoked values:{payload}")
    return payload