import pandas as pd
import streamlit as st
from scripts.db_connect import get_connection

st.set_page_config(page_title="GamePulse Dashboard", layout="wide")
st.title("GamePulse: Video Game Analytics Dashboard")


@st.cache_data
def run_query(query: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()


games_df = run_query("""
    SELECT game_id, title, total_sales, total_revenue, avg_rating, total_reviews, total_playtime
    FROM game_performance
    ORDER BY total_revenue DESC
    LIMIT 10;
""")

players_df = run_query("""
    SELECT player_id, username, total_purchases, total_reviews, total_playtime
    FROM player_activity
    ORDER BY total_playtime DESC
    LIMIT 10;
""")

genre_df = run_query("""
    SELECT genre_name, total_revenue, total_purchases
    FROM revenue_by_genre
    ORDER BY total_revenue DESC;
""")

top_games_df = run_query("""
    SELECT title, total_sales, avg_rating
    FROM top_games
    LIMIT 10;
""")


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Games in View", len(games_df))

with col2:
    st.metric("Top Players Shown", len(players_df))

with col3:
    st.metric("Genres", len(genre_df))


st.subheader("Top Games")
st.dataframe(top_games_df, use_container_width=True)

st.subheader("Game Performance")
st.dataframe(games_df, use_container_width=True)

st.subheader("Player Activity")
st.dataframe(players_df, use_container_width=True)

st.subheader("Revenue by Genre")
st.dataframe(genre_df, use_container_width=True)
st.bar_chart(genre_df.set_index("genre_name")["total_revenue"])