import mysql.connector
from sqlalchemy import create_engine

class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Disconnected from MySQL!")

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def import_dataframe_to_table(self, dataframe, table_name):
        try:
            engine = create_engine(f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{self.database}")
            dataframe.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            print(f"DataFrame imported into '{table_name}' table successfully!")
        except Exception as e:
            import traceback
            print(f"Error: {e}")
            traceback.print_exc()

