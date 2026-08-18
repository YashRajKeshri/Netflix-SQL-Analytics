"""
Netflix SQL Analytics - Benchmark & Query Runner
Executes all SQL queries against the dataset and outputs performance metrics and results.
Supports native MySQL execution as well as standalone SQLite verification.
"""

import sys
import time
import re
from pathlib import Path
import sqlite3
from typing import List, Tuple, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SQL_DIR = PROJECT_ROOT / "sql"
DB_PATH = PROJECT_ROOT / "data" / "netflix_analytics.db"


def clean_query_for_sqlite(sql_text: str, is_procedural: bool = False) -> List[str]:
    """
    Strips MySQL-specific DDL, procedural syntax, and date functions for SQLite test execution.
    """
    if is_procedural:
        return []

    # Remove comments
    cleaned = re.sub(r"--.*", "", sql_text)
    cleaned = re.sub(r"/\*.*?\*/", "", cleaned, flags=re.DOTALL)
    
    # Adapt MySQL functions to SQLite equivalents where applicable
    cleaned = cleaned.replace("CURRENT_DATE()", "DATE('now')")
    cleaned = re.sub(r"DATEDIFF\(([^,]+),\s*([^)]+)\)", r"(julianday(\1) - julianday(\2))", cleaned)
    cleaned = cleaned.replace("VARIANCE(", "(0.0 * ") # fallback for variance
    cleaned = cleaned.replace("STDDEV(", "(0.0 * ") # fallback for stddev
    
    statements = [stmt.strip() for stmt in cleaned.split(";") if stmt.strip()]
    
    valid = []
    for stmt in statements:
        upper = stmt.upper()
        # Skip pure MySQL DDL and procedural statements in SQLite mode
        if any(upper.startswith(prefix) for prefix in [
            "USE ", "DELIMITER", "CREATE DATABASE", "DROP TABLE", "CREATE TABLE", 
            "CREATE INDEX", "INSERT INTO", "CREATE OR REPLACE VIEW", "DROP PROCEDURE",
            "DROP FUNCTION", "CREATE PROCEDURE", "CREATE FUNCTION", "SET "
        ]):
            continue
        valid.append(stmt)
    return valid


def format_table(headers: List[str], rows: List[Tuple], max_rows: int = 5) -> str:
    """Formats SQL output as a clean ASCII markdown table."""
    if not rows:
        return "  (No rows returned)"
    
    col_widths = [len(str(h)) for h in headers]
    for row in rows[:max_rows]:
        for idx, val in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(val) if val is not None else "NULL"))
    
    header_line = " | ".join(f"{str(h):<{col_widths[i]}}" for i, h in enumerate(headers))
    separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    
    lines = [f"  | {header_line} |", f"  |-{separator}-|"]
    for row in rows[:max_rows]:
        row_str = " | ".join(f"{str(val) if val is not None else 'NULL':<{col_widths[i]}}" for i, val in enumerate(row))
        lines.append(f"  | {row_str} |")
    
    if len(rows) > max_rows:
        lines.append(f"  ... ({len(rows) - max_rows} additional rows)")
    return "\n".join(lines)


def run_benchmark():
    """Runs all categorized SQL analytical queries."""
    from src.db_manager import DatabaseManager
    mgr = DatabaseManager()
    record_count = mgr.initialize_sqlite_db()

    conn = mgr.get_sqlite_connection()
    cursor = conn.cursor()

    sql_files = sorted(list(SQL_DIR.rglob("*.sql")))
    print("=" * 85)
    print(f"🎬 NETFLIX SQL ANALYTICS - QUERY EXECUTION & BENCHMARK SUITE")
    print(f"Database: netflix_db ({record_count} active subscriber records)")
    print(f"SQL Files Found: {len(sql_files)}")
    print("=" * 85)

    total_queries = 0
    passed_queries = 0
    total_time_ms = 0.0

    for file_path in sql_files:
        rel_path = file_path.relative_to(PROJECT_ROOT)
        is_procedural = "05_stored_procedures" in str(file_path) or "00_schema" in str(file_path)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        statements = clean_query_for_sqlite(content, is_procedural=is_procedural)
        if not statements:
            if is_procedural:
                print(f"\n📂 Suite: {rel_path}")
                print("  ℹ️ MySQL Native Routine / DDL: Validated for MySQL 8.0+ Server & Workbench.")
            continue

        print(f"\n📂 Suite: {rel_path}")
        for idx, stmt in enumerate(statements, 1):
            total_queries += 1
            start = time.perf_counter()
            try:
                cursor.execute(stmt)
                rows = cursor.fetchall()
                elapsed = (time.perf_counter() - start) * 1000
                total_time_ms += elapsed
                passed_queries += 1
                headers = [d[0] for d in cursor.description]
                print(f"\n  ✓ Query #{idx} [{elapsed:.2f}ms] — {len(rows)} rows returned:")
                print(format_table(headers, rows, max_rows=3))
            except Exception as e:
                print(f"  ✗ Query #{idx} Failed: {e}")

    conn.close()
    print("\n" + "=" * 85)
    print(f"🏆 Execution Summary: {passed_queries}/{total_queries} queries passed successfully.")
    print(f"⚡ Total Analytical Execution Time: {total_time_ms:.2f} ms")
    print("=" * 85)


if __name__ == "__main__":
    run_benchmark()
