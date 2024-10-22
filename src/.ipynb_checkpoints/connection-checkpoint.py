from minio import Minio
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_date, date_format
from delta import *

builder = SparkSession.builder.appName("minio_app") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder, extra_packages=["org.apache.hadoop:hadoop-aws:3.3.4"]).getOrCreate()

# add confs
sc = spark.sparkContext
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "refatorandocourse")
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "refatorandocourse")
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://localhost:9000")
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")
sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")


client = Minio(
    "127.0.0.1:9000",
    access_key="tester",
    secret_key="tester123",
    secure=False
)

minio_bucket = "delta-lake-medallion"

found = client.bucket_exists(minio_bucket)
if not found:
    client.make_bucket(minio_bucket)

data_csv = './stage/hotel_booking.csv'
data_df = spark.read.format('csv').option('header', 'true').option('inferSchema', 'true').load(data_csv)

# Adicionar a nova coluna 'anomesdia' com a data atual
data_df = data_df.withColumn('anomesdia', date_format(current_date(), 'yyyy-MM-dd'))

data_df \
    .write \
    .format("delta") \
    .partition("anomesdia") \
    .mode("overwrite") \
    .save(f"s3a://{minio_bucket}/bronze")
