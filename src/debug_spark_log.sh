#!/bin/bash

# Diretório onde os logs estão armazenados
LOG_DIR="/tmp/spark-logs"  # Altere para o diretório onde seus logs estão

# Verifica se o diretório de logs existe
if [ ! -d "$LOG_DIR" ]; then
    echo "Diretório de logs não encontrado: $LOG_DIR"
    exit 1
fi

# Obtém o último arquivo de log
LOG_FILE=$(ls -t "$LOG_DIR"/* 2>/dev/null | head -n 1)

# Verifica se algum arquivo de log foi encontrado
if [ -z "$LOG_FILE" ]; then
    echo "Nenhum arquivo de log encontrado em: $LOG_DIR"
    exit 1
fi

# Extrai informações sobre o aplicativo, Jobs, SQL Execution e Executor Metrics
echo "Processando arquivo: $LOG_FILE"

echo "Informações sobre o Aplicativo:"
jq 'select(.Event == "SparkListenerApplicationStart") | {AppID: .["App ID"], AppName: .["App Name"], StartTime: .["Time"]}' "$LOG_FILE"

echo "Informações sobre Jobs:"
jq 'select(.Event == "SparkListenerJobEnd") | {JobID: .["Job ID"], CompletionTime: .["Completion Time"], Result: .["Job Result"]["Result"]}' "$LOG_FILE"

echo "Informações sobre SQL Execution:"
jq 'select(.Event == "org.apache.spark.sql.execution.ui.SparkListenerSQLExecutionEnd") | {ExecutionID: .executionId, Time: .time, ErrorMessage: .errorMessage}' "$LOG_FILE"

echo "Tentando capturar métricas de executores:"
jq 'select(.Event == "SparkListenerTaskEnd") | {ExecutorID: .["Task Info"]["Executor ID"], Metrics: .["Task Info"]["Metrics"]}' "$LOG_FILE" | jq 'select(.Metrics != null) | {Metrics: (.Metrics | map({(.Name): .Value}) | add)}'

# Captura eventos de adição e remoção de executores
echo "Informações sobre executores adicionados:"
jq 'select(.Event == "SparkListenerExecutorAdded") | {ExecutorID: .["Executor ID"], TotalCores: .["Total Cores"]}' "$LOG_FILE"

echo "Informações sobre executores removidos:"
jq 'select(.Event == "SparkListenerExecutorRemoved") | {ExecutorID: .["Executor ID"], Reason: .["Reason"]}' "$LOG_FILE"

echo "---------------------------------------"
