"""
Netflix SQL Analytics - Database Manager
Provides unified connection, schema execution, and data loading for MySQL and SQLite testing.
"""

import os
import sqlite3
import csv
from pathlib import Path
from typing import Optional, Dict, Any, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "netflix_users.csv"
SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "sample_netflix_users.csv"
SQL_DIR = PROJECT_ROOT / "sql"


class DatabaseManager:
    """Manages database connection, table initialization, and query execution."""

    def __init__(self, use_mysql: bool = False, mysql_config: Optional[Dict[str, Any]] = None):
        self.use_mysql = use_mysql
        self.mysql_config = mysql_config or {
            "host": os.getenv("MYSQL_HOST", "localhost"),
            "port": int(os.getenv("MYSQL_PORT", 3306)),
            "user": os.getenv("MYSQL_USER", "root"),
            "password": os.getenv("MYSQL_PASSWORD", ""),
            "database": os.getenv("MYSQL_DATABASE", "netflix_db"),
        }
        self.sqlite_db_path = PROJECT_ROOT / "data" / "netflix_analytics.db"

    def get_sqlite_connection(self) -> sqlite3.Connection:
        """Returns a connection to the local SQLite database."""
        conn = sqlite3.connect(self.sqlite_db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_mysql_connection(self):
        """Returns a connection to MySQL server using mysql-connector or pymysql."""
        try:
            import mysql.connector
            return mysql.connector.connect(**self.mysql_config)
        except ImportError:
            try:
                import pymysql
                return pymysql.connect(**self.mysql_config)
            except ImportError:
                raise ImportError(
                    "Neither mysql-connector-python nor pymysql is installed. "
                    "Please install with `pip install mysql-connector-python`."
                )

    def initialize_sqlite_db(self, csv_filepath: Optional[Path] = None) -> int:
        """Initializes SQLite database with schema and loads CSV dataset."""
        csv_file = csv_filepath or DATA_PATH
        if not csv_file.exists():
            csv_file = SAMPLE_DATA_PATH

        conn = self.get_sqlite_connection()
        cursor = conn.cursor()

        # Create table
        cursor.execute("DROP TABLE IF EXISTS netflix_users;")
        cursor.execute("""
            CREATE TABLE netflix_users (
                User_ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Age INTEGER NOT NULL,
                Country TEXT NOT NULL,
                Subscription_Type TEXT NOT NULL,
                Watch_Time_Hours REAL NOT NULL,
                Favorite_Genre TEXT NOT NULL,
                Last_Login TEXT NOT NULL,
                Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_country ON netflix_users (Country);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_subscription ON netflix_users (Subscription_Type);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_genre ON netflix_users (Favorite_Genre);")

        inserted_count = 0
        if csv_file.exists():
            with open(csv_file, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows_to_insert = [
                    (
                        int(row["User_ID"]),
                        row["Name"].strip(),
                        int(row["Age"]),
                        row["Country"].strip(),
                        row["Subscription_Type"].strip(),
                        float(row["Watch_Time_Hours"]),
                        row["Favorite_Genre"].strip(),
                        row["Last_Login"].strip(),
                    )
                    for row in reader
                ]
                cursor.executemany("""
                    INSERT INTO netflix_users (
                        User_ID, Name, Age, Country, Subscription_Type, 
                        Watch_Time_Hours, Favorite_Genre, Last_Login
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """, rows_to_insert)
                inserted_count = len(rows_to_insert)

        conn.commit()
        conn.close()
        return inserted_count


if __name__ == "__main__":
    mgr = DatabaseManager()
    count = mgr.initialize_sqlite_db()
    print(f"✅ Successfully initialized database with {count} records.")
