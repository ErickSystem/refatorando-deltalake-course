from pyspark.sql import SparkSession
import logging

def main():
    MINIO_ACCESS_KEY = "pkIeKAn4xpjoOgXiHQPw"
    MINIO_SECRET_KEY = "JZRBfRszxLZzPeaAQaEXk32JxUKv25DVjUoO06Rk"
    DATABASE = "default"
    BUCKET_BRONZE = "bronze"
    BUCKET_SILVER = "silver"
    BUCKET_GOLD = "gold"

    spark = SparkSession.builder \
        .master("spark://spark-master:7077") \
        .appName("MyAppM6Class02") \
        .config("log4j.rootCategory", "INFO, console") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.316,io.delta:delta-core_2.12:2.4.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.executor.instances", "4") \
        .config("spark.executor.cores", "2") \
        .config("spark.executor.memory", "1536m") \
        .config("spark.driver.memory", "1536m") \
        .config("spark.sql.shuffle.partitions", "16") \
        .config("spark.storage.memoryFraction", "0.4") \
        .config("spark.shuffle.memoryFraction", "0.5") \
        .config("spark.memory.offHeap.enabled", "true") \
        .config("spark.memory.offHeap.size", "512m") \
        .config("spark.sql.parquet.compression.codec", "gzip") \
        .config("spark.sql.orc.compression.codec", "zlib") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.executor.extraJavaOptions", "-XX:+UseG1GC") \
        .config("spark.cleaner.referenceTracking.cleanCheckpoints", "true") \
        .config("spark.executor.cleanupOnShutdown", "true") \
        .getOrCreate()

    sc = spark.sparkContext
    hadoop_conf = sc._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3a.access.key", MINIO_ACCESS_KEY)
    hadoop_conf.set("fs.s3a.secret.key", MINIO_SECRET_KEY)
    hadoop_conf.set("fs.s3a.endpoint", "http://minio:9000")
    hadoop_conf.set("fs.s3a.path.style.access", "true")
    hadoop_conf.set("fs.s3a.connection.ssl.enabled", "false")

    # Testar a conexão com MinIO escrevendo um DataFrame na bucket bronze
    data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
    columns = ["Name", "Age"]
    df = spark.createDataFrame(data, columns)
    df.write.mode("overwrite").parquet(f"s3a://{BUCKET_BRONZE}/test_data.parquet")
    logging.info(f"Dados escritos na bucket {BUCKET_BRONZE}")

    # Ler de volta os dados para verificar
    df_read = spark.read.parquet(f"s3a://{BUCKET_BRONZE}/test_data.parquet")
    df_read.show()

    # Encerrar a SparkSession
    spark.stop()

if __name__ == "__main__":
    main()
