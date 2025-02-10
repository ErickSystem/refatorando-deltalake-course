from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TestMINIOAccess") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# hadoop_conf = spark._jsc.hadoopConfiguration()
sc = spark.sparkContext
hadoop_conf = sc._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", "pkIeKAn4xpjoOgXiHQPw")
hadoop_conf.set("fs.s3a.secret.key", "JZRBfRszxLZzPeaAQaEXk32JxUKv25DVjUoO06Rk")
hadoop_conf.set("fs.s3a.endpoint", "http://minio:9000")
hadoop_conf.set("fs.s3a.path.style.access", "true")
hadoop_conf.set("fs.s3a.connection.ssl.enabled", "false")
hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(hadoop_conf)
path = spark._jvm.org.apache.hadoop.fs.Path("bronze/delta/clothes_batch_bronze/_delta_log")

try:
    statuses = fs.listStatus(path)
    for status in statuses:
        print(status.getPath().toString())
except Exception as e:
    print("Erro ao listar _delta_log:", e)
finally:
    spark.stop()
