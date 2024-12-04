from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import sys

sys.path.insert(0, '/opt/airflow/code')
from src.runner import (
    load_trained_model, encode_data, predict_phenotype, decode_data, update_database, display_results
)

default_args = {
    'start_date': datetime(2024, 11, 20),  # Set your desired start date
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'owner': 'airflow'
}

with DAG(
    'evolife_inference_pipeline',
    default_args=default_args,
    description='Evo Life Inference Dag',
    schedule_interval=None, 
    catchup=False,
) as dag:

    # Define the tasks
    load_trained_model_task = PythonOperator(
        task_id='load_trained_model',
        python_callable=load_trained_model,
    )

    encode_gene_task = PythonOperator(
        task_id='encode_gene',
        python_callable=encode_data,
    )

    predict_phenotype_task = PythonOperator(
        task_id='predict_phenotype',
        python_callable=predict_phenotype,
        provide_context=True, 
    )

    decode_phenotype_task = PythonOperator(
        task_id='decode_phenotype',
        python_callable=decode_data,
        provide_context=True,
    )

    upload_gene_task = PythonOperator(
        task_id='upload_gene',
        python_callable=update_database,
        provide_context=True,
    )

    upload_phenotype_task = PythonOperator(
        task_id='upload_phenotype',
        python_callable=update_database,
        provide_context=True,
    )

    display_results_task = PythonOperator(
        task_id='display_results',
        python_callable=display_results,
        provide_context=True,
    )

    # Define the task dependencies
    encode_gene_task >> upload_gene_task >> display_results_task
    [load_trained_model_task, encode_gene_task] >> predict_phenotype_task >> decode_phenotype_task >> upload_phenotype_task >> display_results_task