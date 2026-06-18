from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    print("data extracted")

def transform():
    print("data transformed")

def load():
    print("data loaded")

with DAG(
    dag_id="dummy_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    extract_task = PythonOperator(
        task_id="extract_task", 
        python_callable=extract
        )
    
    transform_task = PythonOperator(
        task_id="transform_task", 
        python_callable=transform
        )
    
    load_task = PythonOperator(
        task_id="load_task", 
        python_callable=load
        )
    
    extract_task >> transform_task >> load_task
