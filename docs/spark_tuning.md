# SPARK PERFOMANCE TUNING

To set up an Apache Spark cluster on a computer with 8 CPUs and 8 GB of RAM, here are some initial configurations to optimize performance:

## General Configuration

Given that you have limited hardware, the configuration will focus on maximizing resource utilization without overloading the system.

## Cluster Parameters

### Number of Executors:

- You can use 4 executors to distribute the workload since you have 8 CPUs.
- This way, each executor can have 2 CPU cores.

### Number of Cores per Executor (spark.executor.cores):

- Configure each executor with 2 CPU cores: `spark.executor.cores = 2`

### Memory Allocation per Executor (`spark.executor.memory`):

- Divide the memory equally, but leave some for the operating system.
- Use approximately 1.5 GB for the driver and distribute the rest to the executors:
- - Memory per executor: `spark.executor.memory = 1.5g`

### Memory for the Driver (spark.driver.memory):

- Allocate 1.5 GB for the driver: `spark.driver.memory = 1.5Gg`

### Off-Heap Memory Configuration for Executors (if you need off-heap memory):

- For off-heap memory usage (useful to avoid excessive Garbage Collection): `spark.memory.offHeap.enabled = true` and `spark.memory.offHeap.size = 512m`

### Spark Parameters for Performance Configuration

#### Number of Partitions (spark.sql.shuffle.partitions):

- Set a smaller number of partitions, considering you only have 8 cores. A good starting value would be `spark.sql.shuffle.partitions = 16`

### Cache Memory (spark.storage.memoryFraction):

- Set a value that allows efficient caching without consuming all available memory. Set it around 0.4: `spark.storage.memoryFraction = 0.4`

### Memory for Task Execution (spark.shuffle.memoryFraction):

- Set it around 0.5 for data-intensive tasks: `spark.shuffle.memoryFraction = 0.5`

### Detailed Configurations

Here are the grouped settings for convenience:

```bash
spark.executor.instances = 4
spark.executor.cores = 2
spark.executor.memory = 1.5g
spark.driver.memory = 1.5g
spark.sql.shuffle.partitions = 16
spark.storage.memoryFraction = 0.4
spark.shuffle.memoryFraction = 0.5
spark.memory.offHeap.enabled = true
spark.memory.offHeap.size = 512m
```

### Additional Adjustments

Data Compression:

- Use compression to reduce memory usage and increase I/O efficiency:

```bash
spark.sql.parquet.compression.codec = gzip
spark.sql.orc.compression.codec = zlib
``` 

### Serialization:

- Use Kryo serialization, which is more efficient than the default Java serialization:

```bash
spark.serializer = org.apache.spark.serializer.KryoSerializer
``` 

### Garbage Collection (GC) Configuration:

- To avoid long pauses due to GC:

```bash
spark.executor.extraJavaOptions = "-XX:+UseG1GC"
```

### Creating a cache jars

1. This step must be executed inside Jupyter using a terminal
```bash
# zip jars downloaded
cd /home/jovyan/.ivy2 && zip -r -9 /home/jovyan/jars/jars.zip jars
# zip jars ceched
cd /home/jovyan/.ivy2 && zip -r -9 /home/jovyan/jars/cache-jars.zip cache
```
2. Uncomment the area from the file: `dockerfile.jupyter` where it has written: **CREATING CACHE JARS**
3. Make it the build again of container: `docker-compose up --build -d jupyter`
