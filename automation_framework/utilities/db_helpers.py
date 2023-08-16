import sqlite3

class DatabaseHelper:
    def __init__(self, db_name="data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        # Create tables if they don't exist
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                city TEXT PRIMARY KEY,
                temperature REAL,
                feels_like REAL
            )''')

    def insert_weather_data(self, city, temperature, feels_like):
        with self.conn:
            self.conn.execute('''
                INSERT OR REPLACE INTO weather_data (city, temperature, feels_like)
                VALUES (?, ?, ?)
            ''', (city, temperature, feels_like))

    def get_weather_data(self, city):
        cursor = self.conn.execute('''
                SELECT temperature, feels_like
                FROM weather_data
                WHERE city = ?
            ''', (city,))
        row = cursor.fetchone()
        if row:
            temperature, feels_like = row
            return temperature, feels_like
        else:
            return None

