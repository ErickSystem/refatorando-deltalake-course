{{ config(
    materialized='view',
    file_format='delta',
    pre_hook=[
      "CREATE TABLE IF NOT EXISTS default.clothes_batch_bronze USING DELTA LOCATION 's3a://bronze/delta/clothes_batch_bronze'"
    ]
) }}

SELECT *
FROM default.clothes_batch_bronze
LIMIT 10;
