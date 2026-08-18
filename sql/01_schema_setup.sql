-- ==============================================================================
-- Netflix Data Analysis Project
-- Step 1: Database & Table Setup
-- Tool: MySQL Workbench (MySQL 8.0+)
-- ==============================================================================

-- 1. Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS netflix_db;
USE netflix_db;

-- 2. Drop table if starting fresh
DROP TABLE IF EXISTS netflix_users;

-- 3. Create the netflix_users table
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

-- 4. Helpful Indexes to make filtering and grouping faster
CREATE INDEX idx_country ON netflix_users (Country);
CREATE INDEX idx_subscription ON netflix_users (Subscription_Type);
CREATE INDEX idx_genre ON netflix_users (Favorite_Genre);

-- ==============================================================================
-- How to load data:
-- 1. In MySQL Workbench, right-click `netflix_users` under SCHEMAS.
-- 2. Click 'Table Data Import Wizard'.
-- 3. Select 'data/netflix_users.csv' and follow the prompts.
-- ==============================================================================
