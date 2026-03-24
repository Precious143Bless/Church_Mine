import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance
    
    def connect(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host='localhost',
                    database='church_registry',
                    user='root',
                    password='your_password'
                )
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()