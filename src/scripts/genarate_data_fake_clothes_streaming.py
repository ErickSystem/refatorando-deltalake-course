import io
import csv
import random
import argparse
import time
from datetime import datetime, timedelta
from minio import Minio
from minio.error import S3Error

# Parser para receber os parâmetros de data
parser = argparse.ArgumentParser(description='Gera dados fakes como eventos a cada 1 minuto, totalizando no máximo 10 arquivos.')
parser.add_argument('--start_date', type=str, required=True, help='Data inicial no formato YYYY-MM-DD')
parser.add_argument('--interval', type=int, required=True, help='Intervalo de geração dos arquivos')
args = parser.parse_args()

# Converte as strings das datas para objetos datetime (inicia à meia-noite do start_date)
start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
interval = args.interval

# Inicializa o tempo atual com a data de início
current_time = start_date

# Configuração do cliente MinIO
minio_client = Minio(
    "minio:9000",  # endpoint do MinIO (ex: localhost:9000)
    access_key="pkIeKAn4xpjoOgXiHQPw",  # sua access key
    secret_key="JZRBfRszxLZzPeaAQaEXk32JxUKv25DVjUoO06Rk",  # sua secret key
    secure=False
)

# Nome do bucket onde os arquivos serão armazenados
bucket_name = "staging"

# Cria o bucket se ele não existir
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)
    print(f"Bucket '{bucket_name}' criado.")
else:
    print(f"Bucket '{bucket_name}' já existe.")

# Listas de produtos e categorias de roupas
produtos = [
    "Camiseta", "Calça Jeans", "Jaqueta", "Vestido", "Blusa",
    "Saia", "Shorts", "Suéter", "Casaco", "Boné", "Tenis", "Oculos"
]

categorias = [
    "Masculino", "Feminino", "Infantil"
]

# Função para gerar preço unitário aleatório (entre 10 e 500 reais)
def gerar_preco():
    return round(random.uniform(10, 500), 2)

# Contador de arquivos criados
file_count = 0

# Loop para gerar 1 arquivo por minuto, no máximo 10 arquivos
while file_count < 10:
    # Usa o horário atual para gerar o timestamp do evento
    now = datetime.now() - timedelta(hours=3)
    event_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    partition_path = current_time.strftime("yearmonthday=%Y-%m-%d")
    
    # Nome do objeto: inclui o timestamp para garantir nomes únicos (ex: event_2025-01-01_14-05-00.csv)
    file_timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    object_name = f"streaming/clothes/{partition_path}/event_{file_timestamp}.csv"
    
    # Cria um buffer em memória para o CSV e escreve o cabeçalho
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["id", "data_venda", "produto", "categoria", "quantidade", "preco_unitario", "preco_total"])
    
    # Gera até 5 registros para o arquivo
    for _ in range(2):
        produto = random.choice(produtos)
        categoria = random.choice(categorias)
        quantidade = random.randint(1, 5)
        preco_unitario = gerar_preco()
        preco_total = round(quantidade * preco_unitario, 2)
        
        # Gera um ID aleatório entre 1000 e 9999 formatado com 4 dígitos
        random_id = random.randint(1000, 9999)
        formatted_id = f"{random_id:04d}"
        
        writer.writerow([formatted_id, event_timestamp, produto, categoria, quantidade, preco_unitario, preco_total])
    
    # Obtém os dados CSV como bytes
    csv_data = csv_buffer.getvalue().encode('utf-8')
    csv_buffer_bytes = io.BytesIO(csv_data)
    size = len(csv_data)
    
    try:
        # Envia o objeto para o bucket no MinIO
        minio_client.put_object(bucket_name, object_name, csv_buffer_bytes, size, content_type='text/csv')
        print(f"Arquivo enviado: {object_name}")
    except S3Error as err:
        print(f"Erro ao enviar o arquivo {object_name}: {err}")
    
    # Incrementa o contador de arquivos
    file_count += 1
    
    # Se já criou 10 arquivos, encerra o processamento
    if file_count >= 10:
        print("Limite de 10 arquivos atingido. Encerrando o processamento.")
        break

    # Aguarda 5 segundos para criar o próximo arquivo
    time.sleep(interval)
