"""
Netflix SQL Analytics - Interactive Analytics Dashboard
Provides an interactive executive dashboard for slicing and dicing Netflix subscriber SQL data.
"""

import os
import sys
from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.db_manager import DatabaseManager


def main():
    try:
        import streamlit as st
    except ImportError:
        print("Streamlit is not installed. Please run: pip install streamlit")
        return

    st.set_page_config(
        page_title="Netflix SQL Analytics",
        page_icon="🍿",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Styling
    st.markdown("""
        <style>
            .main-header {
                font-size: 2.2rem;
                font-weight: 800;
                color: #E50914;
                margin-bottom: 0px;
            }
            .sub-header {
                font-size: 1rem;
                color: #888888;
                margin-bottom: 25px;
            }
            .metric-card {
                background-color: #1a1a1a;
                border-radius: 10px;
                padding: 15px;
                border-left: 4px solid #E50914;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-header">🍿 Netflix SQL Analytics & BI Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Executive Platform Intelligence, Subscriber Segmentation & Monetization Yield</div>', unsafe_allow_html=True)

    # Initialize DB
    mgr = DatabaseManager()
    if not (PROJECT_ROOT / "data" / "netflix_analytics.db").exists():
        mgr.initialize_sqlite_db()
    
    conn = mgr.get_sqlite_connection()
    cursor = conn.cursor()

    # Sidebar Filters
    st.sidebar.header("🔍 Global Filters")
    
    cursor.execute("SELECT DISTINCT Country FROM netflix_users ORDER BY Country;")
    countries = [r[0] for r in cursor.fetchall()]
    selected_country = st.sidebar.selectbox("Country / Market", ["All"] + countries)

    cursor.execute("SELECT DISTINCT Subscription_Type FROM netflix_users ORDER BY Subscription_Type;")
    tiers = [r[0] for r in cursor.fetchall()]
    selected_tier = st.sidebar.selectbox("Subscription Tier", ["All"] + tiers)

    cursor.execute("SELECT DISTINCT Favorite_Genre FROM netflix_users ORDER BY Favorite_Genre;")
    genres = [r[0] for r in cursor.fetchall()]
    selected_genre = st.sidebar.selectbox("Favorite Genre", ["All"] + genres)

    # Filtered Query
    where_clauses = []
    params = []
    if selected_country != "All":
        where_clauses.append("Country = ?")
        params.append(selected_country)
    if selected_tier != "All":
        where_clauses.append("Subscription_Type = ?")
        params.append(selected_tier)
    if selected_genre != "All":
        where_clauses.append("Favorite_Genre = ?")
        params.append(selected_genre)

    where_str = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    
    # KPI Query
    kpi_query = f"""
        SELECT 
            COUNT(User_ID) AS Total_Users,
            ROUND(AVG(Age), 1) AS Avg_Age,
            ROUND(AVG(Watch_Time_Hours), 1) AS Avg_Watch_Hours,
            ROUND(SUM(Watch_Time_Hours), 0) AS Total_Watch_Hours,
            ROUND(SUM(CASE 
                WHEN Subscription_Type = 'Basic' THEN 9.99
                WHEN Subscription_Type = 'Standard' THEN 15.49
                WHEN Subscription_Type = 'Premium' THEN 22.99
                ELSE 0.00 
            END), 2) AS Estimated_MRR
        FROM netflix_users
        {where_str};
    """
    cursor.execute(kpi_query, params)
    kpi = cursor.fetchone()

    # Metrics Display
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Subscribers", f"{kpi['Total_Users']:,}")
    with col2:
        st.metric("Estimated MRR", f"${kpi['Estimated_MRR']:,.2f}")
    with col3:
        st.metric("Total Streamed", f"{kpi['Total_Watch_Hours']:,} hrs")
    with col4:
        st.metric("Avg Watch Time", f"{kpi['Avg_Watch_Hours']} hrs")
    with col5:
        st.metric("Average Age", f"{kpi['Avg_Age']} yrs")

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Regional & Tier Breakdown", "⚡ SQL Query Studio", "👥 Subscriber Data Browser"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Regional Engagement & Age Profile")
            reg_query = f"""
                SELECT 
                    Country,
                    COUNT(User_ID) AS Users,
                    ROUND(AVG(Watch_Time_Hours), 2) AS Avg_Watch_Hours,
                    ROUND(AVG(Age), 1) AS Avg_Age
                FROM netflix_users
                {where_str}
                GROUP BY Country
                ORDER BY Users DESC;
            """
            cursor.execute(reg_query, params)
            reg_rows = [dict(r) for r in cursor.fetchall()]
            st.dataframe(reg_rows, use_container_width=True)

        with c2:
            st.subheader("Subscription Tier & Genre Affinity")
            tier_query = f"""
                SELECT 
                    Subscription_Type,
                    Favorite_Genre,
                    COUNT(User_ID) AS Users,
                    ROUND(AVG(Watch_Time_Hours), 2) AS Avg_Hours
                FROM netflix_users
                {where_str}
                GROUP BY Subscription_Type, Favorite_Genre
                ORDER BY Users DESC;
            """
            cursor.execute(tier_query, params)
            tier_rows = [dict(r) for r in cursor.fetchall()]
            st.dataframe(tier_rows, use_container_width=True)

    with tab2:
        st.subheader("Interactive MySQL / SQL Studio")
        st.info("Execute custom SELECT analytical queries directly against the database.")
        default_query = "SELECT Country, Subscription_Type, COUNT(*) as Users, ROUND(AVG(Watch_Time_Hours), 2) as Avg_Hours FROM netflix_users GROUP BY Country, Subscription_Type ORDER BY Country, Users DESC;"
        user_sql = st.text_area("SQL Query", value=default_query, height=120)
        
        if st.button("🚀 Run Query"):
            try:
                cursor.execute(user_sql)
                results = cursor.fetchall()
                if results:
                    headers = [d[0] for d in cursor.description]
                    data = [dict(zip(headers, row)) for row in results]
                    st.success(f"Returned {len(results)} rows.")
                    st.dataframe(data, use_container_width=True)
                else:
                    st.warning("Query executed successfully with 0 rows returned.")
            except Exception as e:
                st.error(f"SQL Execution Error: {e}")

    with tab3:
        st.subheader("Raw Subscriber Records")
        raw_query = f"SELECT * FROM netflix_users {where_str} ORDER BY User_ID LIMIT 100;"
        cursor.execute(raw_query, params)
        raw_data = [dict(r) for r in cursor.fetchall()]
        st.dataframe(raw_data, use_container_width=True)

    conn.close()


if __name__ == "__main__":
    main()
