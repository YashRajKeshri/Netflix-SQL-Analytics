# 🐬 MySQL Workbench & Server Setup Guide

Step-by-step instructions to run and execute the **Netflix SQL Analytics** project inside **MySQL Workbench**, MySQL CLI, or cloud MySQL instances.

---

## 🛠️ Step 1: Open MySQL Workbench & Connect

1. Launch **MySQL Workbench**.
2. Connect to your local MySQL instance (e.g. `localhost:3306` with user `root`).

---

## 🏗️ Step 2: Execute Schema & Table DDL

1. In MySQL Workbench, click **File** ➡️ **Open SQL Script...** (or press `Cmd + O` on Mac / `Ctrl + O` on Windows).
2. Select [`sql/00_schema_and_setup/01_create_database_and_tables.sql`](file:///Users/yashkeshri/.gemini/antigravity/scratch/netflix-sql-analytics/sql/00_schema_and_setup/01_create_database_and_tables.sql).
3. Click the ⚡ **Execute** (lightning bolt) icon to run the entire script.
4. Refresh the **SCHEMAS** sidebar on the left to verify that `netflix_db` and table `netflix_users` are created with all indexes.

---

## 📥 Step 3: Populate Dataset

You can choose either of the two methods:

### Option A: Quick Seed Data (Recommended for instant testing)
1. Open [`data/seed_data.sql`](file:///Users/yashkeshri/.gemini/antigravity/scratch/netflix-sql-analytics/data/seed_data.sql) in MySQL Workbench.
2. Click ⚡ **Execute**.

### Option B: Table Data Import Wizard (For Full CSV Import)
1. In MySQL Workbench Schemas pane, right-click `netflix_users` table under `netflix_db`.
2. Select **Table Data Import Wizard**.
3. Browse and select `netflix_users.csv`.
4. Keep the target table as `netflix_users`, map the columns, and click **Next** to complete the import.

---

## 📊 Step 4: Run Analytical Queries

Open and run any analytical script across the categorized folders:

- **Exploratory Data Analysis**: [`sql/01_exploratory_data_analysis/`](file:///Users/yashkeshri/.gemini/antigravity/scratch/netflix-sql-analytics/sql/01_exploratory_data_analysis/)
- **Engagement & Behavior**: [`sql/02_engagement_and_behavior/`](file:///Users/yashkeshri/.gemini/antigravity/scratch/netflix-sql-analytics/sql/02_engagement_and_behavior/)
- **Monetization & MRR**: [`sql/03_revenue_and_monetization/`](file:///Users/yashkeshri/.gemini/antigravity/scratch/netflix-sql-analytics/sql/03_revenue_and_monetization/)
- **Window Functions**: [`sql/04_advanced_window_functions/`](file:///Users/yashkeshri/.gemini/antigravity/scratch/netflix-sql-analytics/sql/04_advanced_window_functions/)
- **Stored Procedures**: [`sql/05_stored_procedures_and_routines/`](file:///Users/yashkeshri/.gemini/antigravity/scratch/netflix-sql-analytics/sql/05_stored_procedures_and_routines/)

To run stored procedures in Workbench:
```sql
USE netflix_db;
CALL sp_GetRegionalReport('USA', 300.00);
CALL sp_GenerateUpsellBatch('Basic', 400.00, 45, 20);
```
