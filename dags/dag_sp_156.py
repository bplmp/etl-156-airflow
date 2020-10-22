from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sqlite_operator import SqliteOperator
from airflow.hooks.sqlite_hook import SqliteHook
from airflow.utils.dates import days_ago

import pandas as pd
import numpy as np
import glob
from datetime import timedelta

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
dag = DAG(
    'sp_156',
    default_args=default_args,
    description='ETL for SP 156 data',
    schedule_interval=timedelta(days=1),
)


def load_clean_and_split_data(**kwargs):
    df = pd.read_csv('data/dados-do-sp156---1o-sem-2020.zip', encoding='iso-8859-1', sep=';')

    # remove rows with empty strings
    df = df[~(df['Órgão'].str.isspace())]

    # split organization into two columns
    df['Órgão'] = df['Órgão'].str.replace('/', '-')
    df['Órgão Principal'] = df['Órgão'].str.split('-').str[0]
    df['Sub-Órgão'] = df['Órgão'].str.split('-').str[1]

    for org in df['Órgão Principal'].unique():
        df_org = df[df['Órgão Principal'] == org]
        df_org.to_csv('exports/organizations/2020-10_' + org.lower() + '.csv', index=False)
        # if you want to save to xslx
        # df_org.to_excel('exports/organizations/2020-10_' + org.lower() + '.xlsx', index=False)


split_data_task = PythonOperator(
    task_id='load_clean_and_split_data',
    depends_on_past=False,
    provide_context=True,
    python_callable=load_clean_and_split_data,
    dag=dag,
)


def load_exported_files(folder):
    files = glob.glob(folder + '/*.csv')
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        dfs.append(df)
    all_dfs = pd.concat(dfs)
    return all_dfs


def summarize_results_per_organization(**kwargs):
    df = load_exported_files('exports/organizations')
    summary = df.groupby(['Órgão Principal', 'Canal'])[['Data de abertura']].count()
    summary = summary.rename(columns={'Data de abertura': 'Número de solicitações'})
    # save file
    summary.to_csv('exports/summaries/2020-10_Resumo Solicitações.csv')


summarize_results_task = PythonOperator(
    task_id='summarize_results_per_organization',
    depends_on_past=False,
    provide_context=True,
    python_callable=summarize_results_per_organization,
    dag=dag,
)

split_data_task >> summarize_results_task
