import sqlite3
import os
import bcrypt
import time

class DatabaseManager:
    def __init__(self):
        self.db_name = f'pc_repair_{int(time.time())}.db'  # Unique database name
        self._create_tables()
        self._create_default_user()

    def _create_tables(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Repair logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS repair_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    issue_type TEXT NOT NULL,
                    description TEXT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error creating tables: {e}")
            if os.path.exists(self.db_name):
                os.remove(self.db_name)
            raise
    
    def _create_default_user(self):
        try:
            if not self.get_user('admin'):
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                
                # Create default admin user with password 'admin123'
                password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    ('admin', password)
                )
                
                conn.commit()
                conn.close()
        except Exception as e:
            print(f"Error creating default user: {e}")
            if os.path.exists(self.db_name):
                os.remove(self.db_name)
            raise
    
    def get_user(self, username):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id, username, password FROM users WHERE username = ?",
                (username,)
            )
            user = cursor.fetchone()
            
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'password': user[2]
                }
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def log_repair(self, issue_type, description, status):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO repair_logs (issue_type, description, status) VALUES (?, ?, ?)",
                (issue_type, description, status)
            )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error logging repair: {e}")
            return False