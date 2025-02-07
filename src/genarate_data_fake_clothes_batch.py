import io
import csv
import random
from datetime import datetime
from minio import Minio
from minio.error import S3Error

# Configuração do cliente MinIO
minio_client = Minio(
    "minio:9000",               # endpoint do MinIO (ex: localhost:9000)
    access_key="pkIeKAn4xpjoOgXiHQPw",        # sua access key
    secret_key="JZRBfRszxLZzPeaAQaEXk32JxUKv25DVjUoO06Rk",        # sua secret key
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

# Lista de produtos e categorias de roupas
produtos = [
    "Camiseta", "Calça Jeans", "Jaqueta", "Vestido", "Blusa",
    "Saia", "Shorts", "Suéter", "Casaco", "Boné", "Tenis", "Oculos"
]

categorias = [
    "Masculino", "Feminino", "Infantil"
]

# Data de início: 1º de janeiro de 2025 (apenas um dia)
start_date = datetime(2025, 1, 1)
date_str = start_date.strftime("%Y-%m-%d")

# Função para gerar preço unitário aleatório (entre 10 e 500 reais)
def gerar_preco():
    return round(random.uniform(10, 500), 2)

# Define a partição e o nome do objeto (ex: yearmonthday=2025-01-01/dia1.csv)
partition_path = f"yearmonthday={date_str}"
object_name = f"batch/clothes/{partition_path}/dia1.csv"

# Cria um buffer em memória para o CSV
csv_buffer = io.StringIO()
writer = csv.writer(csv_buffer)

# Escreve o cabeçalho
writer.writerow(["id", "data_venda", "produto", "categoria", "quantidade", "preco_unitario", "preco_total"])

# Gera 20 registros para o dia, com IDs de 1 a 20
for registro_id in range(1, 21):
    data_venda = date_str
    produto = random.choice(produtos)
    categoria = random.choice(categorias)
    quantidade = random.randint(1, 5)
    preco_unitario = gerar_preco()
    preco_total = round(quantidade * preco_unitario, 2)
    
    writer.writerow([registro_id, data_venda, produto, categoria, quantidade, preco_unitario, preco_total])

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
