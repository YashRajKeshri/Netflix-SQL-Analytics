-- ==============================================================================
-- Netflix Data Analysis Project
-- Step 3: Business Insights & Engagement Analysis
-- Description: Core analytical queries answering key questions about user behavior,
--              popular genres, regional engagement, and revenue.
-- ==============================================================================

USE netflix_db;

-- ------------------------------------------------------------------------------
-- Q6: Regional Engagement Breakdown by Country & Subscription Tier
-- (Analyzes average age and watch hours for each plan within every country)
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- Q7: Subscription Tier vs. Favorite Genre Breakdown
-- (Finds which genres are most popular across Basic, Standard, and Premium tiers)
-- ------------------------------------------------------------------------------
SELECT 
    Subscription_Type,
    Favorite_Genre,
    COUNT(*) AS total_users,
    ROUND(AVG(Watch_Time_Hours), 1) AS avg_watch_time,
    ROUND(SUM(Watch_Time_Hours), 1) AS total_watch_time
FROM netflix_users
GROUP BY Subscription_Type, Favorite_Genre
ORDER BY Subscription_Type, total_users DESC;


-- ------------------------------------------------------------------------------
-- Q8: Age Group Analysis (Demographic Cohorts)
-- (Groups users into Under 25, 25-40, 41-60, 60+ to see viewing patterns)
-- ------------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN Age < 25 THEN 'Under 25'
        WHEN Age BETWEEN 25 AND 40 THEN '25 - 40'
        WHEN Age BETWEEN 41 AND 60 THEN '41 - 60'
        ELSE 'Above 60'
    END AS age_group,
    COUNT(*) AS total_users,
    ROUND(AVG(Watch_Time_Hours), 1) AS avg_watch_hours,
    ROUND(AVG(CASE WHEN Subscription_Type = 'Premium' THEN 1 ELSE 0 END) * 100, 1) AS pct_premium_users
FROM netflix_users
GROUP BY age_group
ORDER BY total_users DESC;


-- ------------------------------------------------------------------------------
-- Q9: Viewer Classification (Heavy, Moderate, Casual)
-- (Segments users based on their total watch hours)
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- Q10: Estimated Monthly Revenue (MRR) by Country & Plan
-- (Basic: $9.99, Standard: $15.49, Premium: $22.99)
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- Q11: Upsell Opportunity: Heavy Viewers on Basic Plans
-- (Users on Basic plan streaming > 500 hours who are good candidates for Premium)
-- ------------------------------------------------------------------------------
SELECT 
    User_ID,
    Name,
    Age,
    Country,
    Subscription_Type,
    Watch_Time_Hours,
    Favorite_Genre,
    Last_Login
FROM netflix_users
WHERE Subscription_Type = 'Basic' 
  AND Watch_Time_Hours >= 500
ORDER BY Watch_Time_Hours DESC
LIMIT 20;
