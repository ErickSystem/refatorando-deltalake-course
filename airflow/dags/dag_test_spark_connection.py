from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['seu_email@exemplo.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dag_test_spark_connection',
    default_args=default_args,
    description='DAG para testar conexão com Spark usando PySpark',
    schedule_interval=None,  # Pode ser executada manualmente
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['teste', 'spark', 'minio'],
) as dag:

    executar_teste_spark = BashOperator(
        task_id='executar_teste_spark',
        bash_command='spark-submit /opt/airflow/scripts/test_spark_connection.py',
    )

    executar_teste_spark
