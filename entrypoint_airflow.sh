#!/bin/bash
set -e

# Espera o MySQL estar disponível
/usr/local/bin/wait-for-it.sh mysql-airflow:3306 --timeout=60 --strict -- echo "MySQL está disponível"

# Inicializa o banco de dados do Airflow
airflow db migrate

# Verifica se o usuário admin já existe
USER_EXISTS=$(airflow users list | grep "${AIRFLOW_ADMIN_USERNAME}" || true)

if [ -z "$USER_EXISTS" ]; then
  echo "Criando o usuário admin..."
  airflow users create \
    --username "${AIRFLOW_ADMIN_USERNAME}" \
    --firstname "${AIRFLOW_ADMIN_FIRSTNAME}" \
    --lastname "${AIRFLOW_ADMIN_LASTNAME}" \
    --role Admin \
    --email "${AIRFLOW_ADMIN_EMAIL}" \
    --password "${AIRFLOW_ADMIN_PASSWORD}"
  echo "Usuário admin criado com sucesso."
else
  echo "Usuário admin já existe."
fi

# Inicia o webserver do Airflow
exec airflow webserver
