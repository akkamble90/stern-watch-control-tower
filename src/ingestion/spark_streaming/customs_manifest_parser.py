from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr

def parse_customs_manifests(input_path: str, output_path: str):
    spark = SparkSession.builder.appName("CustomsManifestParser").getOrCreate()
    df = spark.read.json(input_path)
    
    clean_df = df.filter(col("declared_weight_kg") > 0) \
                 .withColumn("is_critical", expr("IF(part_number LIKE 'MCU%', True, False)"))
                 
    clean_df.write.mode("overwrite").parquet(output_path)
    print(f"Successfully processed customs manifests to {output_path}")

if __name__ == "__main__":
    parse_customs_manifests("data/sample_manifests/", "data/mocks/processed_manifests")