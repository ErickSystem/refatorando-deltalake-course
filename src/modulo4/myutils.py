from minio import Minio
from minio.error import S3Error


def remove_location(client, bucket_name, folder_prefix):
    # Configurações do cliente MinIO
    try:
        # Verifica se o bucket existe
        if client.bucket_exists(bucket_name):
            # Lista todos os objetos dentro da pasta específica
            objects_to_delete = client.list_objects(bucket_name, prefix=folder_prefix, recursive=True)
            objects_list = [obj.object_name for obj in objects_to_delete]
    
            if objects_list:
                # Deleta todos os objetos encontrados
                for obj_name in objects_list:
                    client.remove_object(bucket_name, obj_name)
                    print(f"Objeto '{obj_name}' deletado.")
    
                print(f"Pasta '{folder_prefix}' deletada com sucesso do bucket '{bucket_name}'.")
            else:
                print(f"A pasta '{folder_prefix}' está vazia ou não existe no bucket '{bucket_name}'.")
        else:
            print(f"O bucket '{bucket_name}' não existe.")
    except S3Error as e:
        print(f"Ocorreu um erro: {e}")

