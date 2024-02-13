import mysql.connector
import sqlite3


class DatabaseManager:
    def __init__(self):
        self.database_name = "database"
        self.database_tables = {
            "patients": ("id INT PRIMARY KEY, name VARCHAR(255), sex VARCHAR(6), age INT, birthdate DATE"),
            "doctors": ("id INT PRIMARY KEY, name VARCHAR(255)")
        }
        self.conn = None
        self.c = None

        self.host = self.get_server_ip_address()
        self.user = "test_user2"
        self.password = "test2"

    def get_server_ip_address(self):
        conn = sqlite3.connect("Database/setup.db")
        c = conn.cursor()

        query = """
            SELECT server_ip_address
            FROM setup
        """

        c.execute(query)

        server_ip_address = c.fetchone()

        return server_ip_address[0]

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.c = self.conn.cursor()
            print("Connected to the MySQL server.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self):
        if self.conn:
            self.c.close()
            self.conn.close()
            print("Disconnected from the MySQL server.")
    
    def create_database(self):
        try:
            self.connect()
            create_db_query = f"CREATE DATABASE IF NOT EXISTS `{self.database_name}`"
            self.c.execute(create_db_query)
            self.conn.commit()
        except Exception as e:
            print(f"Error in create_database: {e}")
        finally:
            self.disconnect()

    def create_tables(self):
        try:
            self.connect()
            use_db_query = f"USE `{self.database_name}`"
            self.c.execute(use_db_query)

            for table_name, table_structure in self.database_tables.items():
                create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({table_structure})"
                self.c.execute(create_table_query)

            self.conn.commit()
        except Exception as e:
            print(f"Error in create_tables: {e}")
        finally:
            self.disconnect()


    def insert_values(self):
        self.connect()
        query = f"USE `{self.database_name}`"
        self.c.execute(query)

        query = """
            INSERT INTO patients (
                id,
                name,
                sex,
                age,
                birthdate
            )
            VALUES (
                1,
                'Jasper Sampang',
                'Male',
                24,
                '2000-02-10'
            )
        """
        self.c.execute(query)
        self.conn.commit()
        self.disconnect()
