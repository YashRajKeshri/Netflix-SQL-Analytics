-- ==============================================================================
-- Netflix Data Analysis Project
-- Step 2: Exploratory Data Analysis (EDA)
-- Description: Basic data inspection, row counts, and summary statistics.
-- ==============================================================================

USE netflix_db;

-- ------------------------------------------------------------------------------
-- Q1: Total records and preview the first 10 rows
-- ------------------------------------------------------------------------------
SELECT COUNT(*) AS total_records FROM netflix_users;

SELECT * FROM netflix_users 
LIMIT 10;


-- ------------------------------------------------------------------------------
-- Q2: Check for distinct countries, subscription plans, and genres
-- ------------------------------------------------------------------------------
SELECT DISTINCT Country FROM netflix_users ORDER BY Country;
SELECT DISTINCT Subscription_Type FROM netflix_users;
SELECT DISTINCT Favorite_Genre FROM netflix_users ORDER BY Favorite_Genre;


-- ------------------------------------------------------------------------------
-- Q3: Summary stats for Age and Watch Time (Min, Max, Average)
-- ------------------------------------------------------------------------------
SELECT 
    MIN(Age) AS min_age,
    ROUND(AVG(Age), 1) AS avg_age,
    MAX(Age) AS max_age,
    MIN(Watch_Time_Hours) AS min_watch_hours,
    ROUND(AVG(Watch_Time_Hours), 1) AS avg_watch_hours,
    MAX(Watch_Time_Hours) AS max_watch_hours
FROM netflix_users;


-- ------------------------------------------------------------------------------
-- Q4: User distribution by Subscription Plan
-- ------------------------------------------------------------------------------
SELECT 
    Subscription_Type,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_users), 2) AS percentage
FROM netflix_users
GROUP BY Subscription_Type
ORDER BY total_users DESC;


-- ------------------------------------------------------------------------------
-- Q5: User count and average watch time by Country
-- ------------------------------------------------------------------------------
SELECT 
    Country,
    COUNT(*) AS total_users,
    ROUND(AVG(Watch_Time_Hours), 2) AS avg_watch_hours,
    ROUND(SUM(Watch_Time_Hours), 2) AS total_watch_hours
FROM netflix_users
GROUP BY Country
ORDER BY total_users DESC;
