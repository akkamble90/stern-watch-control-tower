from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from config.settings import settings

def start_spark_telemetry_stream():
    # Updated SparkSession with Maven packages for Kafka streaming and PostgreSQL JDBC
    spark = SparkSession.builder \
        .appName("Mercedes_ControlTower_TelemetryStream") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.6.0") \
        .config("spark.sql.streaming.schemaInference", "true") \
        .getOrCreate()

    schema = StructType([
        StructField("container_id", StringType(), False),
        StructField("vessel_imo_or_truck_id", StringType(), False),
        StructField("transport_mode", StringType(), False),
        StructField("latitude", DoubleType(), False),
        StructField("longitude", DoubleType(), False),
        StructField("speed_knots_or_kmh", DoubleType(), True),
        StructField("ambient_temp_celsius", DoubleType(), True),
        StructField("destination_plant", StringType(), False),
        StructField("timestamp", TimestampType(), False)
    ])

    raw_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", settings.kafka_bootstrap_servers) \
        .option("subscribe", settings.kafka_telemetry_topic) \
        .load()

    parsed_stream = raw_stream \
        .selectExpr("CAST(value AS STRING) as json_val") \
        .select(from_json(col("json_val"), schema).alias("data")) \
        .select("data.*")

    processed_stream = parsed_stream \
        .withColumn("thermal_anomaly", when(col("ambient_temp_celsius") > 45.0, True).otherwise(False)) \
        .withColumn("congestion_flag", when(col("speed_knots_or_kmh") < 1.0, True).otherwise(False))

    query = processed_stream.writeStream \
        .format("console") \
        .outputMode("append") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    start_spark_telemetry_stream()