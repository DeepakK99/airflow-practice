from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

attempt_counter = {"count": 0}

def flaky_task():
    attempt_counter["count"] += 1

    print(f"Attempt {attempt_counter['count']}")

    if attempt_counter["count"] < 3:
        print(f"count: {attempt_counter['count']}")
        raise Exception("Temporary failure")

    print("Success!")

with DAG(
    dag_id="retry_demo",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    task = PythonOperator(
        task_id="flaky_task",
        python_callable=flaky_task,
        retries=2,
        retry_delay=timedelta(seconds=20),
    )