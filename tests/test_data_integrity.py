"""
Data Quality & Integrity Tests for Netflix SQL Analytics
"""

import sys
import unittest
from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.db_manager import DatabaseManager


class TestDataQuality(unittest.TestCase):
    """Verifies schema constraints and domain integrity."""

    @classmethod
    def setUpClass(cls):
        cls.mgr = DatabaseManager()
        cls.mgr.initialize_sqlite_db()
        cls.conn = cls.mgr.get_sqlite_connection()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_no_null_user_ids(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM netflix_users WHERE User_ID IS NULL;")
        null_count = cursor.fetchone()[0]
        self.assertEqual(null_count, 0, "User_ID must not contain NULL values.")

    def test_valid_subscription_plans(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT Subscription_Type FROM netflix_users;")
        plans = {r[0] for r in cursor.fetchall()}
        valid_plans = {"Basic", "Standard", "Premium"}
        self.assertTrue(plans.issubset(valid_plans), f"Unexpected plans found: {plans - valid_plans}")

    def test_age_range_boundaries(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT MIN(Age), MAX(Age) FROM netflix_users;")
        min_age, max_age = cursor.fetchone()
        self.assertGreaterEqual(min_age, 10, "Minimum age must be >= 10.")
        self.assertLessEqual(max_age, 120, "Maximum age must be <= 120.")

    def test_non_negative_watch_time(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM netflix_users WHERE Watch_Time_Hours < 0;")
        invalid_hours = cursor.fetchone()[0]
        self.assertEqual(invalid_hours, 0, "Watch_Time_Hours cannot be negative.")


if __name__ == "__main__":
    unittest.main()
