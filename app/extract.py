import os.path

from pyspark.sql import SparkSession
import psycopg2
from pyspark.sql.functions import *
from pyspark.sql.functions import lit
import numpy as np

file_path = os.path.abspath("Behavioral_Risk_Factor_Surveillance_System_data.csv")

spark = SparkSession.builder \
    .appName("SQLite Example") \
    .master("local[*]") \
    .getOrCreate()

db_path = os.path.abspath("../healthyheartDB")
db_url = f"jdbc:sqlite:{db_path}"

df = spark.read.csv(file_path, header=True, inferSchema=True)
try:
    conn = psycopg2.connect(db_url)
    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print("PostgreSQL version:", version)
    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print("Error connecting to the database:", e)

filtered_data = df.filter(df["Year"] > 2014)
grouped_data = filtered_data.groupby("Locationdesc", "Class") \
    .agg({"Sample_Size": "sum"}) \
    .withColumnRenamed("sum(Sample_Size)", "Total_Sample_Size")

print(db_url)
grouped_data.show(4)

grouped_data.write \
    .format("jdbc") \
    .option("url", db_url) \
    .option("driver", "org.sqlite.JDBC") \
    .option("dbtable", "healthyheart") \
    .mode("overwrite") \
    .save()


spark.stop()
