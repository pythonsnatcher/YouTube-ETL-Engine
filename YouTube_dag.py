from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from youtube_api_etl import main


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


from datetime import timedelta

dag = DAG(
    'youtube_dag',
    default_args=default_args,
    description='A simple DAG to fetch YouTube data',
    schedule=timedelta(days=1),  
)


run_etl = PythonOperator(
    task_id='run_youtube_etl',
    python_callable=main,
    dag=dag,
)

run_etl
