from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

# Definir argumentos padrão para a DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['seu_email@exemplo.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Função Python que gera logs
def tarefa_python_func(**kwargs):
    logging.info("Esta é uma mensagem de INFO da tarefa Python.")
    logging.warning("Esta é uma mensagem de WARNING da tarefa Python.")
    logging.error("Esta é uma mensagem de ERROR da tarefa Python.")
    print("A mensagem foi impressa no console.")

# Definir a DAG
with DAG(
    'dag_teste_logs',
    default_args=default_args,
    description='Uma DAG de teste para verificar logs no Airflow',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['teste', 'logs'],
) as dag:

    # Tarefa 1: Iniciar a DAG
    iniciar_dag = BashOperator(
        task_id='iniciar_dag',
        bash_command='echo "Iniciando a DAG de teste para logs"',
    )

    # Tarefa 2: Executar função Python que gera logs
    gerar_logs = PythonOperator(
        task_id='gerar_logs',
        python_callable=tarefa_python_func,
        provide_context=True,
    )

    # Tarefa 3: Finalizar a DAG
    finalizar_dag = BashOperator(
        task_id='finalizar_dag',
        bash_command='echo "Finalizando a DAG de teste para logs"',
    )

    # Definir a ordem das tarefas
    iniciar_dag >> gerar_logs >> finalizar_dag
