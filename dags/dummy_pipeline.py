from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

def extract_customer():
    print("customer data extracted")

def extract_shipment():
    print("shipment data extracted")

def validate_customer():
    print("customer validation completed")

def validate_shipment():
    print("shipment validation completed")

def build_silver():
    print("silver tables built")

def build_gold():
    print("gold tables built")

def build_metrices():
    print("metrices tables built")

def load():
    print("successfully loaded")


with DAG(
    dag_id="dummy_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    extract_customer_task = PythonOperator(
        task_id="extract_customer_task", 
        python_callable=extract_customer
        )
    
    extract_shipment_task = PythonOperator(
        task_id="extract_shipment_task", 
        python_callable=extract_shipment
        )
    
    validate_customer_task = PythonOperator(
        task_id="validate_customer_task", 
        python_callable=validate_customer
        )
    
    validate_shipment_task = PythonOperator(
        task_id="validate_shipment_task", 
        python_callable=validate_shipment
        )
    
    build_silver_task = PythonOperator(
        task_id="build_silver_task", 
        python_callable=build_silver
        )
    
    build_gold_task = PythonOperator(
        task_id="build_gold_task", 
        python_callable=build_gold
        )
    
    build_metrices_task = PythonOperator(
        task_id="build_metrices_task", 
        python_callable=build_metrices
        )
    
    load_task = PythonOperator(
        task_id="load_task", 
        python_callable=load
        )
    
    # extract & validate for customer and shipment in paralle

    # option 1
    # start >> extract_customer_task >> validate_customer_task
    # start >> extract_shipment_task >> validate_shipment_task
    # [validate_customer_task, validate_shipment_task] >> build_silver_task
    # build_silver_task >> build_gold_task >> build_metrices_task
    # build_metrices_task >> load_task
    # load_task >> end

    # option 2
    start >> [extract_customer_task, extract_shipment_task]
    extract_customer_task >> validate_customer_task
    extract_shipment_task >> validate_shipment_task
    [validate_customer_task, validate_shipment_task] >> build_silver_task
    build_silver_task >> build_gold_task >> build_metrices_task
    build_metrices_task >> load_task
    load_task >> end
