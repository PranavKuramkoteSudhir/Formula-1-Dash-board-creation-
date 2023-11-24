from pyspark.sql import SparkSession

class PySparkMySQLExtractor:
    def __init__(self, connection_properties):
        self.connection_properties = connection_properties
        self.spark = SparkSession.builder \
            .appName("PySparkMySQLExtractor") \
            .config("spark.jars", "/Users/pranav/Downloads/mysql-connector-j-8.2.0/mysql-connector-j-8.2.0.jar") \
            .getOrCreate()
    def extract_table_to_pandas(self, table_name):
        # Read data from MySQL
        df = self.spark.read.format("jdbc") \
            .option("url", self.connection_properties["url"]) \
            .option("dbtable", table_name) \
            .option("user", self.connection_properties["user"]) \
            .option("password", self.connection_properties["password"]) \
            .option("driver", self.connection_properties["driver"]) \
            .load()

        # Convert PySpark DataFrame to Pandas DataFrame
        pandas_df = df.toPandas()
        df.unpersist()
        return pandas_df

    def close_spark_session(self):

        self.spark.stop()


