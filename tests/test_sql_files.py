"""
Unit & Integration Tests for Netflix SQL Analytics Queries
"""

import sys
import unittest
from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.db_manager import DatabaseManager
from src.run_sql_benchmark import clean_query_for_sqlite


class TestNetflixSQLAnalytics(unittest.TestCase):
    """Test suite validating SQL scripts and analytical pipelines."""

    @classmethod
    def setUpClass(cls):
        cls.mgr = DatabaseManager()
        cls.record_count = cls.mgr.initialize_sqlite_db()
        cls.conn = cls.mgr.get_sqlite_connection()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_database_has_records(self):
        """Verify that subscriber records were successfully loaded."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM netflix_users;")
        count = cursor.fetchone()[0]
        self.assertGreater(count, 0, "Database must contain subscriber records.")

    def test_schema_setup_script(self):
        """Verify schema setup script exists."""
        sql_file = PROJECT_ROOT / "sql" / "01_schema_setup.sql"
        self.assertTrue(sql_file.exists())

    def test_exploratory_data_analysis_queries(self):
        """Test EDA queries return rows."""
        sql_file = PROJECT_ROOT / "sql" / "02_exploratory_data_analysis.sql"
        self.assertTrue(sql_file.exists())
        with open(sql_file, "r", encoding="utf-8") as f:
            content = f.read()

        statements = clean_query_for_sqlite(content)
        cursor = self.conn.cursor()
        for stmt in statements:
            cursor.execute(stmt)
            rows = cursor.fetchall()
            self.assertGreater(len(rows), 0)

    def test_business_insights_queries(self):
        """Test business insights queries execute cleanly."""
        sql_file = PROJECT_ROOT / "sql" / "03_engagement_and_business_insights.sql"
        self.assertTrue(sql_file.exists())
        with open(sql_file, "r", encoding="utf-8") as f:
            content = f.read()

        statements = clean_query_for_sqlite(content)
        cursor = self.conn.cursor()
        for stmt in statements:
            cursor.execute(stmt)
            rows = cursor.fetchall()
            self.assertGreater(len(rows), 0)

    def test_advanced_sql_queries(self):
        """Test CTEs and Window Functions."""
        sql_file = PROJECT_ROOT / "sql" / "04_advanced_sql_techniques.sql"
        self.assertTrue(sql_file.exists())
        with open(sql_file, "r", encoding="utf-8") as f:
            content = f.read()

        statements = clean_query_for_sqlite(content)
        cursor = self.conn.cursor()
        for stmt in statements:
            cursor.execute(stmt)
            rows = cursor.fetchall()
            self.assertGreater(len(rows), 0)

    def test_master_script(self):
        """Test master script execution."""
        sql_file = PROJECT_ROOT / "netflix_sql_analysis.sql"
        self.assertTrue(sql_file.exists())
        with open(sql_file, "r", encoding="utf-8") as f:
            content = f.read()

        statements = clean_query_for_sqlite(content)
        cursor = self.conn.cursor()
        for stmt in statements:
            cursor.execute(stmt)
            rows = cursor.fetchall()
            self.assertGreater(len(rows), 0)


if __name__ == "__main__":
    unittest.main()
