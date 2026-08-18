# 📖 Netflix SQL Analytics - Data Dictionary & Schema Documentation

Comprehensive technical documentation for the `netflix_db` relational schema, column definitions, constraints, performance indexing, and calculated business metrics.

---

## 🏛️ Entity: `netflix_users`

The primary transactional and profile entity representing individual streaming platform subscribers.

### Column Specifications

| Column Name | MySQL Data Type | Constraints | Nullable | Description | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`User_ID`** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | ❌ No | Unique surrogate key identifying each subscriber | `1`, `2`, `1004` |
| **`Name`** | `VARCHAR(100)` | `NOT NULL` | ❌ No | Full name of the subscriber | `'James Martinez'`, `'Jane Smith'` |
| **`Age`** | `TINYINT UNSIGNED` | `CHECK (Age >= 10 AND Age <= 120)` | ❌ No | Age in years of the primary account holder | `18`, `35`, `68` |
| **`Country`** | `VARCHAR(50)` | `NOT NULL` | ❌ No | Geographic market / country of residence | `'USA'`, `'UK'`, `'France'`, `'Canada'` |
| **`Subscription_Type`** | `ENUM('Basic', 'Standard', 'Premium')` | `NOT NULL` | ❌ No | Active subscription tier level | `'Basic'`, `'Standard'`, `'Premium'` |
| **`Watch_Time_Hours`** | `DECIMAL(7, 2)` | `CHECK (Watch_Time_Hours >= 0.00)` | ❌ No | Cumulative hours spent streaming content | `80.26`, `615.93`, `909.30` |
| **`Favorite_Genre`** | `ENUM('Action', 'Comedy', 'Drama', 'Documentary', 'Horror', 'Romance', 'Sci-Fi')` | `NOT NULL` | ❌ No | Primary self-selected or algorithmic top genre | `'Sci-Fi'`, `'Action'`, `'Drama'` |
| **`Last_Login`** | `DATE` | `NOT NULL` | ❌ No | Calendar date of most recent platform session | `'2025-02-05'`, `'2024-10-30'` |
| **`Created_At`** | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | ❌ No | System audit timestamp of account creation | `2024-01-15 08:30:00` |
| **`Updated_At`** | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | ❌ No | System audit timestamp of last row update | `2025-02-18 12:00:00` |

---

## ⚡ Indexing Strategy

| Index Identifier | Target Column(s) | Index Type | Query Optimization Objective |
| :--- | :--- | :--- | :--- |
| `pk_netflix_users` | `User_ID` | B-Tree (Clustered) | O(1) primary key lookups & referential integrity |
| `idx_netflix_country` | `Country` | B-Tree | Optimizes geographic filtering and regional grouping |
| `idx_netflix_subscription` | `Subscription_Type` | B-Tree | Accelerates subscription tier and revenue aggregations |
| `idx_netflix_genre` | `Favorite_Genre` | B-Tree | Accelerates content affinity and genre ranking |
| `idx_netflix_last_login` | `Last_Login` | B-Tree | Optimizes recency, churn risk, and date range scans |
| `idx_netflix_country_tier` | `(Country, Subscription_Type)` | B-Tree (Composite) | Eliminates filesort for multi-dimensional regional reports |
| `idx_netflix_tier_genre` | `(Subscription_Type, Favorite_Genre)` | B-Tree (Composite) | Covers tier-genre affinity matrix queries |
| `idx_netflix_country_watchtime` | `(Country, Watch_Time_Hours)` | B-Tree (Composite) | Covers regional window ranking (`RANK() OVER (PARTITION BY Country...)`) |

---

## 📐 Business Metric & Formula Definitions

### 1. Monthly Recurring Revenue (MRR)
\[
\text{MRR} = \sum (\text{Basic Users} \times \$9.99) + (\text{Standard Users} \times \$15.49) + (\text{Premium Users} \times \$22.99)
\]

### 2. Annual Recurring Revenue (ARR)
\[
\text{ARR} = \text{MRR} \times 12
\]

### 3. Average Revenue Per User (ARPU)
\[
\text{ARPU} = \frac{\text{Total MRR}}{\text{Total Active Subscribers}}
\]

### 4. Revenue Yield per Streamed Hour
\[
\text{Yield} = \frac{\text{Monthly Revenue (\USD)}}{\text{Total Streamed Hours}}
\]
