import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
            cls._instance.cursor = None
        return cls._instance
    
    def connect(self):
        """Establish database connection"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host='localhost',
                    database='church_registry',
                    user='root',
                    password='your_password',
                    charset='utf8mb4',
                    use_unicode=True
                )
                self.cursor = self.connection.cursor(dictionary=True)
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def execute_query(self, query, params=None):
        """Execute a query with parameters"""
        try:
            self.connect()
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor
        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return None
    
    def fetch_all(self, query, params=None):
        """Fetch all results"""
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchall()
        return []
    
    def fetch_one(self, query, params=None):
        """Fetch one result"""
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchone()
        return None
    
    def insert(self, table, data):
        """Insert data into table"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor = self.execute_query(query, tuple(data.values()))
        if cursor:
            return cursor.lastrowid
        return None
    
    def update(self, table, data, where_clause, where_params):
        """Update data in table"""
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        params = tuple(data.values()) + where_params
        cursor = self.execute_query(query, params)
        return cursor.rowcount if cursor else 0
    
    def delete(self, table, where_clause, where_params):
        """Delete data from table"""
        query = f"DELETE FROM {table} WHERE {where_clause}"
        cursor = self.execute_query(query, where_params)
        return cursor.rowcount if cursor else 0
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def __del__(self):
        """Destructor to close connection"""
        self.close()


# Convenience functions for common operations
def get_db():
    """Get database connection instance"""
    return DatabaseConnection()


def init_database():
    """Initialize database tables if they don't exist"""
    db = get_db()
    db.connect()
    
    # Create tables
    tables = {
        'members': """
            CREATE TABLE IF NOT EXISTS members (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                middle_name VARCHAR(100),
                last_name VARCHAR(100) NOT NULL,
                suffix VARCHAR(20),
                birth_date DATE NOT NULL,
                gender VARCHAR(1) NOT NULL,
                civil_status VARCHAR(20) NOT NULL,
                address TEXT NOT NULL,
                contact_number VARCHAR(20) NOT NULL,
                email VARCHAR(100),
                occupation VARCHAR(100),
                spouse_name VARCHAR(200),
                date_registered DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                INDEX idx_name (last_name, first_name),
                INDEX idx_active (is_active)
            )
        """,
        'sacraments': """
            CREATE TABLE IF NOT EXISTS sacraments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                member_id INT NOT NULL,
                sacrament_type VARCHAR(50) NOT NULL,
                date_received DATE NOT NULL,
                officiating_priest VARCHAR(200) NOT NULL,
                church_location VARCHAR(200),
                godfather VARCHAR(200),
                godmother VARCHAR(200),
                confirmation_name VARCHAR(100),
                sponsor VARCHAR(200),
                spouse VARCHAR(200),
                witnesses TEXT,
                remarks TEXT,
                certificate_number VARCHAR(50),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
                INDEX idx_type (sacrament_type),
                INDEX idx_date (date_received)
            )
        """,
        'pledges': """
            CREATE TABLE IF NOT EXISTS pledges (
                id INT AUTO_INCREMENT PRIMARY KEY,
                member_id INT NOT NULL,
                pledge_description VARCHAR(200) NOT NULL,
                amount_promised DECIMAL(10,2) NOT NULL,
                due_date DATE NOT NULL,
                pledge_date DATE DEFAULT CURRENT_DATE,
                status VARCHAR(20) DEFAULT 'Unpaid',
                notes TEXT,
                FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
                INDEX idx_status (status),
                INDEX idx_due_date (due_date)
            )
        """,
        'payments': """
            CREATE TABLE IF NOT EXISTS payments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                pledge_id INT NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                payment_date DATE NOT NULL,
                payment_method VARCHAR(50) NOT NULL,
                reference_number VARCHAR(100),
                received_by VARCHAR(100) NOT NULL,
                receipt_number VARCHAR(50),
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pledge_id) REFERENCES pledges(id) ON DELETE CASCADE,
                INDEX idx_date (payment_date),
                INDEX idx_method (payment_method)
            )
        """
    }
    
    for table_name, create_sql in tables.items():
        db.execute_query(create_sql)
        print(f"Table '{table_name}' ensured")
    
    print("Database initialization complete")


# Run initialization if this script is executed directly
if __name__ == "__main__":
    init_database()