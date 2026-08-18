-- ==============================================================================
-- Netflix Data Analysis Project
-- Step 4: Intermediate SQL Techniques (CTEs & Window Functions)
-- Description: Using RANK(), DENSE_RANK(), and Common Table Expressions (WITH).
-- ==============================================================================

USE netflix_db;

-- ------------------------------------------------------------------------------
-- Q12: Top 3 Most Active Streamers in Each Country
-- (Uses ROW_NUMBER / RANK to find the biggest watchers in every market)
-- ------------------------------------------------------------------------------
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


-- ------------------------------------------------------------------------------
-- Q13: Most Popular Genre in Each Country
-- (Uses a CTE and DENSE_RANK to find the #1 genre by watch time for every country)
-- ------------------------------------------------------------------------------
WITH GenrePopularity AS (
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
FROM GenrePopularity
WHERE genre_rank = 1
ORDER BY total_hours DESC;


-- ------------------------------------------------------------------------------
-- Q14: Percentage Contribution of Each Subscription Plan per Country
-- (Uses SUM() OVER (PARTITION BY ...) window function)
-- ------------------------------------------------------------------------------
SELECT 
    Country,
    Subscription_Type,
    COUNT(*) AS users_in_tier,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Country), 1) AS pct_of_country_users
FROM netflix_users
GROUP BY Country, Subscription_Type
ORDER BY Country, users_in_tier DESC;
