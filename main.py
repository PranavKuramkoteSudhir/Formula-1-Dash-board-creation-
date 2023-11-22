import mysql_connect
from csv_to_df import CsvToDf
import time
from schema_creation_sql import F1Schema
from sqlalchemy import create_engine

# Initialize MySQLConnector
mysql_connector = mysql_connect.MySQLConnector("127.0.0.1", "root", "", "")
mysql_connector.connect()
F1Schema(mysql_connector)
mysql_connector.disconnect()
mysql_connector = mysql_connect.MySQLConnector("127.0.0.1", "root", "", "formula2")
mysql_connector.connect()
# Initialize CsvToDf
csvtodf = CsvToDf()
df = csvtodf.get_df_dict()

# Define table names
table_names = ["constructors", "drivers", "circuits", "races", "lap_times", "pit_stops", "qualifying", "results" ]

# Loop through table names and import DataFrames into MySQL tables
for name in table_names:
    time.sleep(1)
    # Get the DataFrame for the current table
    current_df = df.get(name)

    # Check if the DataFrame exists before importing
    if current_df is not None:
        # Create an SQLAlchemy engine for the MySQL connection
        engine = create_engine(
            f"mysql+mysqlconnector://{mysql_connector.user}:{mysql_connector.password}@{mysql_connector.host}/{mysql_connector.database}")

        # Import the DataFrame into the MySQL table
        mysql_connector.import_dataframe_to_table(current_df, name)

# Disconnect from MySQL
mysql_connector.disconnect()
