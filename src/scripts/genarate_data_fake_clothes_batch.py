import io
import csv
import random
import argparse
from datetime import datetime, timedelta
from minio import Minio
from minio.error import S3Error

# Parser para receber os parâmetros de data
parser = argparse.ArgumentParser(description='Gera dados fakes para um período específico.')
parser.add_argument('--start_date', type=str, required=True, help='Data inicial no formato YYYY-MM-DD')
parser.add_argument('--end_date', type=str, required=True, help='Data final no formato YYYY-MM-DD')
args = parser.parse_args()

# Converte as strings das datas para objetos datetime
start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
end_date = datetime.strptime(args.end_date, '%Y-%m-%d')

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

# Loop para percorrer cada dia do período
current_date = start_date
while current_date <= end_date:
    # Formata a data atual como string (ex: "2025-01-01")
    date_str = current_date.strftime("%Y-%m-%d")
    
    # Define a partição e o nome do objeto (ex: yearmonthday=2025-01-01/2025-01-01.csv)
    partition_path = f"yearmonthday={date_str}"
    object_name = f"batch/clothes/{partition_path}/{date_str}.csv"
    
    # Cria um buffer em memória para o CSV
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    
    # Escreve o cabeçalho
    writer.writerow(["id", "data_venda", "produto", "categoria", "quantidade", "preco_unitario", "preco_total"])
    
    # Gera 20 registros para o dia com IDs aleatórios de até 4 dígitos
    for _ in range(20):
        data_venda = date_str
        produto = random.choice(produtos)
        categoria = random.choice(categorias)
        quantidade = random.randint(1, 5)
        preco_unitario = gerar_preco()
        preco_total = round(quantidade * preco_unitario, 2)
        
        # Gera um ID aleatório entre 1 e 9999 e o formata como string de 4 dígitos
        random_id = random.randint(1000, 9999)
        formatted_id = f"{random_id:04d}"
        
        writer.writerow([formatted_id, data_venda, produto, categoria, quantidade, preco_unitario, preco_total])
    
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
    
    # Incrementa a data para o próximo dia
    current_date += timedelta(days=1)
