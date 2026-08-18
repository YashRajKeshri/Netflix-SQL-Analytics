-- ==============================================================================
-- 🎬 NETFLIX USER DATA ANALYSIS (MySQL)
-- Author: Yash Raj Keshri
-- Dataset: netflix_users.csv (25,000 subscriber records)
-- Dialect: MySQL 8.0+ / MySQL Workbench
-- ==============================================================================

-- ==============================================================================
-- PART 1: DATABASE & TABLE SETUP
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS netflix_db;
USE netflix_db;

DROP TABLE IF EXISTS netflix_users;

CREATE TABLE netflix_users (
    User_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Age INT NOT NULL,
    Country VARCHAR(50) NOT NULL,
    Subscription_Type VARCHAR(20) NOT NULL,
    Watch_Time_Hours DECIMAL(7, 2) NOT NULL,
    Favorite_Genre VARCHAR(50) NOT NULL,
    Last_Login DATE NOT NULL
);

-- Note: Import `data/netflix_users.csv` via MySQL Workbench 'Table Data Import Wizard'
-- or use the seed data if testing quickly.


-- ==============================================================================
-- PART 2: EXPLORATORY DATA ANALYSIS (EDA)
-- ==============================================================================

-- Q1: Total records and preview top 10 users
SELECT COUNT(*) AS total_records FROM netflix_users;
SELECT * FROM netflix_users LIMIT 10;

-- Q2: Check distinct countries, subscription plans, and genres
SELECT DISTINCT Country FROM netflix_users ORDER BY Country;
SELECT DISTINCT Subscription_Type FROM netflix_users;
SELECT DISTINCT Favorite_Genre FROM netflix_users ORDER BY Favorite_Genre;

-- Q3: Summary statistics for Age and Watch Hours
SELECT 
    MIN(Age) AS min_age,
    ROUND(AVG(Age), 1) AS avg_age,
    MAX(Age) AS max_age,
    MIN(Watch_Time_Hours) AS min_watch_hours,
    ROUND(AVG(Watch_Time_Hours), 1) AS avg_watch_hours,
    MAX(Watch_Time_Hours) AS max_watch_hours
FROM netflix_users;

-- Q4: Subscription Plan Distribution
SELECT 
    Subscription_Type,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_users), 2) AS percentage
FROM netflix_users
GROUP BY Subscription_Type
ORDER BY total_users DESC;


-- ==============================================================================
-- PART 3: BUSINESS & ENGAGEMENT INSIGHTS
-- ==============================================================================

-- Q5: Regional Engagement: Breakdown by Country & Subscription Tier
-- (Shows average age and watch hours for every plan in each country)
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

-- Q6: Favorite Genre by Subscription Tier
-- (Shows which genres users prefer on Basic vs Standard vs Premium)
SELECT 
    Subscription_Type,
    Favorite_Genre,
    COUNT(*) AS total_users,
    ROUND(AVG(Watch_Time_Hours), 1) AS avg_watch_time,
    ROUND(SUM(Watch_Time_Hours), 1) AS total_watch_time
FROM netflix_users
GROUP BY Subscription_Type, Favorite_Genre
ORDER BY Subscription_Type, total_users DESC;

-- Q7: Age Demographic Cohorts
SELECT 
    CASE 
        WHEN Age < 25 THEN 'Under 25'
        WHEN Age BETWEEN 25 AND 40 THEN '25 - 40'
        WHEN Age BETWEEN 41 AND 60 THEN '41 - 60'
        ELSE 'Above 60'
    END AS age_group,
    COUNT(*) AS total_users,
    ROUND(AVG(Watch_Time_Hours), 1) AS avg_watch_hours
FROM netflix_users
GROUP BY age_group
ORDER BY total_users DESC;

-- Q8: Viewer Segmentation (Heavy vs Moderate vs Casual)
SELECT 
    CASE 
        WHEN Watch_Time_Hours >= 700 THEN 'Heavy Streamer (700+ hrs)'
        WHEN Watch_Time_Hours >= 300 THEN 'Moderate Streamer (300-699 hrs)'
        ELSE 'Casual Streamer (<300 hrs)'
    END AS streamer_type,
    COUNT(*) AS user_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_users), 1) AS pct_of_users,
    ROUND(AVG(Watch_Time_Hours), 1) AS avg_hours
FROM netflix_users
GROUP BY streamer_type
ORDER BY avg_hours DESC;

-- Q9: Estimated Monthly Revenue (MRR) by Country
-- Pricing assumption: Basic = $9.99, Standard = $15.49, Premium = $22.99
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

-- Q10: Upsell Candidates: Heavy Streamers on Basic Plan (>500 hrs)
SELECT 
    User_ID,
    Name,
    Age,
    Country,
    Subscription_Type,
    Watch_Time_Hours,
    Favorite_Genre
FROM netflix_users
WHERE Subscription_Type = 'Basic' AND Watch_Time_Hours >= 500
ORDER BY Watch_Time_Hours DESC
LIMIT 20;


-- ==============================================================================
-- PART 4: INTERMEDIATE WINDOW FUNCTIONS & CTES
-- ==============================================================================

-- Q11: Top 3 Most Active Streamers per Country using RANK()
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

-- Q12: #1 Favorite Genre in Each Country using DENSE_RANK()
WITH CountryGenreRank AS (
    SELECT 
        Country,
        Favorite_Genre,
        COUNT(*) AS total_fans,
        ROUND(SUM(Watch_Time_Hours), 1) AS total_hours,
        DENSE_RANK() OVER (PARTITION BY Country ORDER BY SUM(Watch_Time_Hours) DESC) AS genre_rank
    FROM netflix_users
    GROUP BY Country, Favorite_Genre
)
SELECT 
    Country,
    Favorite_Genre AS top_genre,
    total_fans,
    total_hours
FROM CountryGenreRank
WHERE genre_rank = 1
ORDER BY total_hours DESC;
