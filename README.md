# 🎬 Netflix User Data Analysis (MySQL)

A practical data analytics project analyzing **25,000 Netflix subscriber records** using **MySQL Workbench (MySQL 8.0+)**. 

This project explores user viewing habits, subscription tier preferences, demographic patterns, genre popularity, and revenue opportunities using SQL queries ranging from basic aggregations to intermediate Common Table Expressions (CTEs) and Window Functions.

---

## 📌 Project Overview

- **Database:** MySQL 8.0+ / MySQL Workbench
- **Dataset:** 25,000 rows (`netflix_users.csv`)
- **Key Concepts:** `GROUP BY`, `HAVING`, `CASE WHEN`, `CTE` (Common Table Expressions), Window Functions (`RANK()`, `DENSE_RANK()`, `SUM() OVER`), Aggregate Functions (`COUNT`, `AVG`, `SUM`, `ROUND`, `MIN`, `MAX`).

---

## 📊 Dataset Structure

The dataset contains subscriber information with 8 main attributes:

| Column | Type | Description |
| :--- | :--- | :--- |
| `User_ID` | `INT` | Unique identifier for each subscriber |
| `Name` | `VARCHAR(100)` | Subscriber's name |
| `Age` | `INT` | Subscriber's age (18 to 75) |
| `Country` | `VARCHAR(50)` | Country (USA, UK, Canada, Germany, France, Brazil, Australia, India, Mexico, Japan) |
| `Subscription_Type` | `VARCHAR(20)` | Plan type: **Basic**, **Standard**, or **Premium** |
| `Watch_Time_Hours` | `DECIMAL(7,2)` | Total hours watched |
| `Favorite_Genre` | `VARCHAR(50)` | Preferred genre (Action, Comedy, Drama, Documentary, Horror, Romance, Sci-Fi) |
| `Last_Login` | `DATE` | Most recent login date |

---

## 📂 Project Files

```
netflix-sql-analytics/
├── netflix_sql_analysis.sql           # Complete all-in-one SQL script for MySQL Workbench
├── sql/
│   ├── 01_schema_setup.sql            # Database and table creation script
│   ├── 02_exploratory_data_analysis.sql # Basic counts, distinct values, summary stats
│   ├── 03_engagement_and_business_insights.sql # Regional breakdown, genre matrix, revenue
│   └── 04_advanced_sql_techniques.sql # CTEs, Window Functions (RANK, DENSE_RANK)
├── data/
│   ├── netflix_users.csv              # Full dataset (25,000 rows)
│   └── seed_data.sql                  # Quick INSERT seed script
├── docs/
│   └── mysql_workbench_guide.md       # Step-by-step setup guide
├── app/
│   └── dashboard.py                   # Optional interactive Streamlit dashboard
├── push_to_github.py                  # Script to upload/sync to GitHub
└── README.md
```

---

## ❓ Business Questions & SQL Queries

### 1. Regional Engagement: Country & Subscription Breakdown
*How do subscriber numbers, average age, and watch time vary across different countries and plans?*

```sql
SELECT 
    Country,
    Subscription_Type,
    COUNT(*) AS total_users,
    ROUND(AVG(Age), 1) AS avg_age,
    ROUND(AVG(Watch_Time_Hours), 1) AS avg_watch_hours,
    ROUND(SUM(Watch_Time_Hours), 1) AS total_watch_hours
FROM netflix_users
GROUP BY Country, Subscription_Type
ORDER BY Country ASC, avg_watch_hours DESC;
```
> **Insight:** Watch time is evenly distributed across countries, but users on Premium plans stream slightly more hours on average compared to Basic plans.

---

### 2. Subscription Tier vs. Favorite Genre Preferences
*Which genres are most popular among Basic, Standard, and Premium subscribers?*

```sql
SELECT 
    Subscription_Type,
    Favorite_Genre,
    COUNT(*) AS total_users,
    ROUND(AVG(Watch_Time_Hours), 1) AS avg_watch_time
FROM netflix_users
GROUP BY Subscription_Type, Favorite_Genre
ORDER BY Subscription_Type, total_users DESC;
```
> **Insight:** Drama, Comedy, and Sci-Fi consistently attract the largest audience across all three subscription plans.

---

### 3. Estimated Monthly Recurring Revenue (MRR) by Country
*Assuming standard pricing (Basic: $9.99, Standard: $15.49, Premium: $22.99), how much monthly revenue does each country generate?*

```sql
SELECT 
    Country,
    COUNT(*) AS total_subscribers,
    ROUND(SUM(CASE 
        WHEN Subscription_Type = 'Basic' THEN 9.99
        WHEN Subscription_Type = 'Standard' THEN 15.49
        WHEN Subscription_Type = 'Premium' THEN 22.99
        ELSE 0 
    END), 2) AS estimated_mrr_usd,
    ROUND(AVG(CASE 
        WHEN Subscription_Type = 'Basic' THEN 9.99
        WHEN Subscription_Type = 'Standard' THEN 15.49
        WHEN Subscription_Type = 'Premium' THEN 22.99
        ELSE 0 
    END), 2) AS avg_revenue_per_user
FROM netflix_users
GROUP BY Country
ORDER BY estimated_mrr_usd DESC;
```
> **Insight:** The platform generates ~$404,300 in estimated MRR across the 25,000 subscribers, with Premium users driving nearly 48% of total revenue.

---

### 4. Upsell Targeting: Heavy Viewers on Basic Plans
*Which subscribers on the Basic plan watch more than 500 hours? (Prime candidates for Premium 4K upgrades)*

```sql
SELECT 
    User_ID,
    Name,
    Age,
    Country,
    Subscription_Type,
    Watch_Time_Hours,
    Favorite_Genre
FROM netflix_users
WHERE Subscription_Type = 'Basic' 
  AND Watch_Time_Hours >= 500
ORDER BY Watch_Time_Hours DESC
LIMIT 20;
```
> **Insight:** Over 4,000 Basic plan users have logged >500 hours of watch time. Targeting them with promotional upgrade offers could significantly increase Average Revenue Per User (ARPU).

---

### 5. Top 3 Most Active Streamers per Country (Window Function: `RANK()`)
*Who are the top 3 biggest streamers in each country?*

```sql
WITH RankedUsers AS (
    SELECT 
        User_ID,
        Name,
        Country,
        Subscription_Type,
        Favorite_Genre,
        Watch_Time_Hours,
        RANK() OVER (PARTITION BY Country ORDER BY Watch_Time_Hours DESC) AS rank_in_country
    FROM netflix_users
)
SELECT 
    Country,
    rank_in_country,
    Name,
    Subscription_Type,
    Favorite_Genre,
    Watch_Time_Hours
FROM RankedUsers
WHERE rank_in_country <= 3
ORDER BY Country, rank_in_country;
```

---

## 💡 Key Takeaways & Recommendations

1. **Revenue Concentration:** Premium subscribers account for **~47.8% of total revenue**, despite making up 33.6% of the subscriber base.
2. **Upsell Opportunities:** A substantial cohort of Basic plan subscribers watch 500+ hours. In-app upgrade prompts highlighting 4K streaming and multiple screens could drive organic plan migration.
3. **Content Affinity:** Sci-Fi and Drama show the highest total engagement hours globally, making them the most effective retention drivers.

---

## 🚀 How to Run in MySQL Workbench

1. Open **MySQL Workbench** and connect to your local MySQL server.
2. Open [`netflix_sql_analysis.sql`](netflix_sql_analysis.sql).
3. Execute Part 1 to create the database and table.
4. Import `data/netflix_users.csv` using the **Table Data Import Wizard** (right-click `netflix_users` > Table Data Import Wizard).
5. Run any query in Part 2, 3, or 4 to see results!

---

## 👤 Author
- **Yash Raj Keshri** ([@YashRajKeshri](https://github.com/YashRajKeshri))
- **License:** MIT
