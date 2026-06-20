from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import time

def long_running_task():
    print("Starting task...")
    time.sleep(30)
    print("Finished")

with DAG(
    dag_id="timeout_demo",
    start_date=datetime(2024,1,1),
    schedule=None,
    catchup=False,
) as dag:

    long_task = PythonOperator(
        task_id="long_task",
        python_callable=long_running_task,
        execution_timeout=timedelta(seconds=10),
    )