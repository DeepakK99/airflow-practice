from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

def process_shipments():
    print("daily shipment data processed")

with DAG(
    dag_id="daily_shipments_dag_temp",
    start_date=datetime(2026, 6, 15),
    schedule='@daily',
    catchup=True,
) as dag:
    process_shipments_task = PythonOperator(
        task_id="process_shipements_task",
        python_callable=process_shipments
    )