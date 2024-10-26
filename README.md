# COURSE TO TEACH ABOUT DELTA LAKE

## SETUP INITIAL ENVIRONMENT

### Operating System Prerequisites

- Docker
- Docker Compose
- Git
- Python>=3.13
- Minio CLI
- VS Code (Optional)

#### Creating Python venv locally

```bash
python3 -m venv .env
# Using
source .env/bin/activate
```

#### Pre commit (Optional)

```bash
pip install pre-commit nbstripout
# pre commit 
pre-commit run --all-files
## Setting up nbstripout directly without to use the pre-commit
nbstripout --install
```


### Installation and Setup:

1. Clone the repository to your local machine.
2. Ensure Docker is installed and running.
3. Navigate to the project directory containing the docker-compose.yml file.
4. Run `docker-compose up -d` to start the services defined in the docker-compose file.
5. Access JUPYTER notebook through `http://localhost:8888` to execute the provided code.
5. Access SPARK UI through `http://localhost:8080`
6. Access MINIO through `http://localhost:9000` (USER: admin PASS: refatorandopass)



### TESTING SPARK CLUSTER ENVIRONMENT AND SETUP

Let's use this notebook below and check it out if we can connect with Spark cluster

- `src/spark_test.ipynb`

Another notebook will be used to test Spark cluster, and the configs required.
It is in this notebook that let's go to make the initial connection between Delta Lake (Processing Layer) and Minio (Repository similar to the AWS S3)

- `src/spark_test_delta_with_minio.ipynb`

### Usage:
1. After setting up the Docker containers, access Jupyter notebook through the provided URL.
2. Use the provided code snippet in a Jupyter notebook or Python environment to interact with Minio using Apache Spark with Delta.
3. Generate the keys in Minio: **access key** and **secret key** and add them inside the `envs.conf` file
4. initialize envs: `source envs.conf`
5. MINIO by CLI

```bash
# Instaling minio MACOS
brew install minio/stable/mc
# Setting up credentials
mc alias set myminio $MINIO_SERVER:$MINIO_PORT $MINIO_ACCESS_KEY $MINIO_SECRET_KEY
# testing credentials listing all buckets
mc ls myminio
# Copy data to stage
mc cp data/hotel_booking.csv myminio/stage/
```

### SPARK PERFOMANCE TUNING

The notebook below contains the optimizations made for our development environment, considering a machine with limited resources. These configs will make our Spark cluster more efficient for our tests while working in the local development environment.

- `src/spark_tuning.ipynb`
- [Learn more about the configurations of this environment](./docs/spark_tuning.md)

### PROJECTS

- [01 Hotel Booking](./docs/projects/01_hotel_booking.md)


