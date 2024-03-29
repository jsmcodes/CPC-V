import mysql.connector
import sqlite3


class DatabaseManager:
    def __init__(self):
        self.database_name = "database"
        self.database_tables = {
            "patients": (
                """
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255),
                    sex VARCHAR(6),
                    age VARCHAR(8),
                    birthdate DATE,
                    contact_number VARCHAR(17),
                    address VARCHAR(255),
                    archived BIT(1) DEFAULT 0
                """
            ),
            "users": (
                """
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    position_id INT,
                    name VARCHAR(255),
                    sex VARCHAR(6),
                    age VARCHAR(8),
                    birthdate DATE,
                    contact_number VARCHAR(17),
                    address VARCHAR(255),
                    username VARCHAR(50),
                    password VARCHAR(50),
                    archived BIT(1) DEFAULT 0
                """
            ),
            "positions": (
                """
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100),
                    archived BIT(1) DEFAULT 0
                """
            ),
            "login_history": (
                """
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT,
                    name VARCHAR(255),
                    position VARCHAR(12),
                    date DATE,
                    time TIME
                """
            ),
            "consultations": (
                """
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    patient_id INT,
                    doctor_id INT,
                    date DATE,
                    time TIME,
                    status VARCHAR(7) DEFAULT 'Waiting',
                    archived BIT(1) DEFAULT 0  
                """
            )
        }
        self.conn = None
        self.c = None
        self.host = self.get_server_ip_address()
        self.user = "mobile_hs"
        self.password = "mobilepass"

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

            query = f"USE `{self.database_name}`"
            self.c.execute(query)
            
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

            for table_name, table_structure in self.database_tables.items():
                create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({table_structure})"
                self.c.execute(create_table_query)

            self.conn.commit()
        except Exception as e:
            print(f"Error in create_tables: {e}")
        finally:
            self.disconnect()

    def insert_positions(self):
        self.connect()

        positions = ("Pediatrician", "OB/GYN", "Receptionist")

        for position in positions:
            query = f"""
                INSERT INTO positions (
                    name
                )
                VALUES (
                    '{position}'
                )
            """
            self.c.execute(query)


        self.conn.commit()
        self.disconnect()

    def insert_users(self):
        self.connect()

        users = (
            (1, 'test_pedia', 'Male', '24y 0m', '2000-02-20', '(+63)912-345-6789', 'Test Address 1', 'user1', 'pass1'),
            (2, 'test_obgyn', 'Female', '47y 4m', '1976-09-20', '(+63)912-345-7856', 'Test Address 2', 'user2', 'pass2'),
            (3, 'test_receptionist', 'Female', '24y 6m', '1999-07-28', '(+63)912-345-3215', 'Test Address 3', 'user3', 'pass3')
        )

        for user in users:
            query = f"""
                INSERT INTO users (
                    position_id,
                    name,
                    sex,
                    age,
                    birthdate,
                    contact_number,
                    address,
                    username,
                    password
                )
                VALUES (
                    {user[0]},
                    '{user[1]}',
                    '{user[2]}',
                    '{user[3]}',
                    '{user[4]}',
                    '{user[5]}',
                    '{user[6]}',
                    '{user[7]}',
                    '{user[8]}'
                )
            """
            self.c.execute(query)


        self.conn.commit()
        self.disconnect()

    def insert_values(self):
        self.connect()

        query = """
            INSERT INTO patients (
                name,
                sex,
                age,
                birthdate,
                contact_number,
                address
            )
            VALUES (
                'Jasper Sampang',
                'Male',
                '24y 0m',
                '2000-02-10',
                '(+63)961-639-3688',
                'B19 L1 Camella General Trias, Brgy San Francisco, General Trias City, Cavite'
            )
        """
        self.c.execute(query)

        self.conn.commit()
        self.disconnect()
