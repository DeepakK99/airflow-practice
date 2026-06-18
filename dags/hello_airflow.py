from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello():
    print("Hello from Airflow")

with DAG(
    dag_id="hello_airflow",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    
    hello_task = PythonOperator(
        task_id="hello_task",
        python_callable=hello,
    )
