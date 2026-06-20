from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def extract_shipments():
    print("Extracting shipment data")


def validate_bronze():
    print("Validating bronze data")


def build_silver():
    print("Building silver layer")


def silver_quality_check():
    print("Checking silver quality")


def build_gold():
    print("Building gold layer")


def generate_metrics():
    print("Generating shipment metrics")


with DAG(
    dag_id="shipment_medallion_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_shipments",
        python_callable=extract_shipments,
    )

    bronze_validation_task = PythonOperator(
        task_id="validate_bronze",
        python_callable=validate_bronze,
    )

    silver_task = PythonOperator(
        task_id="build_silver",
        python_callable=build_silver,
    )

    quality_task = PythonOperator(
        task_id="silver_quality_check",
        python_callable=silver_quality_check,
    )

    gold_task = PythonOperator(
        task_id="build_gold",
        python_callable=build_gold,
    )

    metrics_task = PythonOperator(
        task_id="generate_metrics",
        python_callable=generate_metrics,
    )

    (
        extract_task
        >> bronze_validation_task
        >> silver_task
        >> quality_task
        >> gold_task
        >> metrics_task
    )