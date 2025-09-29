import pytest
#from prove import trigger_lambda_mock
import boto3

# fixture che prepara dati e funzione

@pytest.fixture
def lambda_payload():
    client = boto3.client("lambda", region_name="us-east-1")
    payload = {
        "my_name": ["Airflow","Windows","Linux"],
        "my_age": [ 25, 30, 35 ],
    }

    print(f"[Lambda] Invoked values:{payload}")
    return payload




def test_trigger_lambda_mock(lambda_payload):
    assert lambda_payload is not None
    assert "my_name" in lambda_payload
    assert type(lambda_payload) == dict

 


