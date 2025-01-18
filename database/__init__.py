import sqlite3
import os
import bcrypt

class DatabaseManager:
    def __init__(self):
        self.db_path = 'pc_repair.db'
        self._create_tables()
        self._create_default_user()

    def _create_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        
        # Create repair_logs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS repair_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            issue_type TEXT NOT NULL,
            description TEXT,
            status TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def _create_default_user(self):
        # Create a default admin user if it doesn't exist
        if not self.get_user('admin'):
            # Hash the default password
            password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO users (username, password) VALUES (?, ?)
            ''', ('admin', password))
            
            conn.commit()
            conn.close()
    
    def get_user(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'password': user[2]
            }
        return None
    
    def log_repair(self, issue_type, description, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO repair_logs (issue_type, description, status)
        VALUES (?, ?, ?)
        ''', (issue_type, description, status))
        
        conn.commit()
        conn.close()