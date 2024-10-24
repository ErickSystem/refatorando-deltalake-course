# CURSO PARA ENSINAR SOBRE DELTA LAKE

## CONFIGURAÇÃO INICIAL DO AMBIENTE

### Operating System Prerequisites

- Docker
- Docker Compose
- Git
- Python>=3.13
- VS Code (Opcional)

#### Creating Python venv locally

```bash
python3 -m venv .env
# Using
source .env/bin/activate
```

### Installation and Setup:

1. Clone the repository to your local machine.
2. Ensure Docker is installed and running.
3. Navigate to the project directory containing the docker-compose.yml file.
4. Run `docker-compose up` to start the services defined in the docker-compose file.
5. Access JUPYTER notebook through `http://localhost:8888` to execute the provided code.
5. Access SPARK UI through `http://localhost:8080`
6. Access MINIO through `http://localhost:9000` (USER: admin PASS: refatorandopass)



### TESTING SPARK CLUSTER ENVIRONMENT AND SETUP

Let's use this notebook below and check it out if we can connect with Spark cluster

- `test_spark.ipynb`

Another notebook will be used to test Spark cluster, and the configs required.
It is in this notebook that let's go to make the initial connection between Delta Lake (Processing Layer) and Minio (Repository similar to the AWS S3)

- `spark_test_con_minio.ipynb`

### Usage:
1. After setting up the Docker containers, access Jupyter notebook through the provided URL.
2. Use the provided code snippet in a Jupyter notebook or Python environment to interact with Minio using Apache Spark with Delta.
3. Modify the code as needed for your specific use case, such as changing the access key, secret key, endpoint, or file paths.

#### MINIO

```bash

# instalando minio MACOS
brew install minio/stable/mc
# Configurando as credenciais
mc alias set myminio $MINIO_SERVER:$MINIO_PORT $MINIO_ACCESS_KEY $MINIO_SECRET_KEY
```

## PROJECT 1 - HOTEL BOOKING

### Description:
This project demonstrates how to use Apache Spark with Delta Lake to interact with Minio, an object storage service, for data storage and manipulation. The setup involves configuring Spark to work with Delta Lake and Minio, and then writing data from a CSV file to Minio in Delta format using Spark.

- [Data source](https://www.kaggle.com/datasets/mojtaba142/hotel-booking)


![alt text](./img/arq_simp_ingestao_dados.jpg)

### Components:

- **Apache Spark with Delta**: Apache Spark is a powerful analytics engine for big data processing, while Delta Lake provides ACID transactions, scalable metadata handling, and unifies streaming and batch data processing. Together, they enable efficient data processing and management.

- **Minio**: Minio is an open-source object storage server compatible with Amazon S3 cloud storage service. It is used here as the data storage solution, allowing for scalable and distributed storage of files in buckets.

- **Jupyter Notebook**: Jupyter Notebook is an interactive computing environment that allows users to create and share documents containing live code, equations, visualizations, and narrative text. It provides an easy-to-use interface for running Python code snippets and visualizing data.

- **Docker Compose**: Docker Compose is a tool for defining and running multi-container Docker applications. It allows developers to define the services, networks, and volumes required for their application in a single YAML file and then spin up the entire application stack with a single command.

#### Configuration:
- Ensure that Minio is running and accessible at `http://localhost:9000`.
- Modify the Minio access key, secret key, and endpoint in the provided code to match your Minio setup.
- Adjust the Docker volumes and environment variables in the docker-compose file as needed.

#### Notes:
- This project assumes a local Minio setup for testing purposes. Adjust configurations accordingly for production environments.
- Ensure proper security measures are implemented, especially when dealing with access keys and secret keys.
- Delta Lake provides ACID transactions, scalable metadata handling, and unifies streaming and batch data processing.
