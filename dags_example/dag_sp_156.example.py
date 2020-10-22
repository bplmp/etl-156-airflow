# import airflow modules
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sqlite_operator import SqliteOperator
from airflow.hooks.sqlite_hook import SqliteHook
from airflow.utils.dates import days_ago

# import other python packages
import pandas as pd
import numpy as np
import glob
from datetime import timedelta

# default arguments for an airflow dag
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# create the dag
dag = DAG(
    'sp_156',
    default_args=default_args,
    description='ETL for SP 156 data',
    schedule_interval=timedelta(days=1),
)


def load_clean_and_split_data(**kwargs):
    # load the data, clean it and split it in several files here
    pass


# create the task for this function
split_data_task = PythonOperator(
    task_id='load_clean_and_split_data',
    depends_on_past=False,
    provide_context=True,
    python_callable=load_clean_and_split_data,
    dag=dag,
)


def summarize_results_per_organization(**kwargs):
    # load the exported files and summarize the results here
    pass


# create the task for this other function
summarize_results_task = PythonOperator(
    task_id='summarize_results_per_organization',
    depends_on_past=False,
    provide_context=True,
    python_callable=summarize_results_per_organization,
    dag=dag,
)

# chain the tasks
split_data_task >> summarize_results_task
