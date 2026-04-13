import pandas as pd
<<<<<<< HEAD
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
=======
import plotly.express as px
import streamlit as st
from scripts.db_connect import get_connection

# ─── Config ───────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="GamePulse",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background-color: #0f0f1a; color: #e0e0e0; }
    section[data-testid="stSidebar"] { background-color: #12122a; }
    h1, h2, h3 { color: #e2e8f0; }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #6c63ff44;
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
        margin-bottom: 8px;
    }
    .metric-label { font-size: 0.8rem; color: #a0aec0; margin-bottom: 4px; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #6c63ff; }
</style>
""", unsafe_allow_html=True)

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e0e0e0",
    margin=dict(t=30, b=30),
    xaxis=dict(gridcolor="#2d2d4e"),
)

# ─── DB ───────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def query(sql, params=None):
    conn = get_connection()
    try:
        df = pd.read_sql(sql, conn, params=params)
        return df
    finally:
        conn.close()
# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🎮 GamePulse")
    st.markdown("*Video Game Analytics*")
    st.divider()

    genres    = query("SELECT DISTINCT genre_name FROM revenue_by_genre ORDER BY genre_name")["genre_name"].tolist()
    platforms = query("SELECT DISTINCT platform_name FROM platforms ORDER BY platform_name")["platform_name"].tolist()

    sel_genres = st.multiselect("Filter by Genre", genres, default=genres)
    sel_plats  = st.multiselect("Filter by Platform", platforms, default=platforms)
    top_n      = st.selectbox("Top N", [5, 10, 15, 20], index=1)

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("# 🎮 GamePulse Analytics Dashboard")
st.markdown("Video game sales, player behavior, and developer performance — powered by PostgreSQL.")
st.divider()

# ─── KPIs ─────────────────────────────────────────────────────────────────────

kpi = query("""
    SELECT
        (SELECT COUNT(*) FROM games)      AS total_games,
        (SELECT COUNT(*) FROM players)    AS total_players,
        (SELECT COUNT(*) FROM purchases)  AS total_purchases,
        (SELECT ROUND(SUM(amount_paid)::numeric, 0) FROM purchases) AS total_revenue,
        (SELECT COUNT(*) FROM developers) AS total_developers,
        (SELECT ROUND(AVG(rating)::numeric, 2) FROM reviews) AS avg_rating
""").iloc[0]

c1, c2, c3, c4, c5, c6 = st.columns(6)
cards = [
    (c1, "🎮 Games",       f"{int(kpi['total_games']):,}"),
    (c2, "👥 Players",     f"{int(kpi['total_players']):,}"),
    (c3, "🛒 Purchases",   f"{int(kpi['total_purchases']):,}"),
    (c4, "💰 Revenue",     f"${int(kpi['total_revenue']):,}"),
    (c5, "🏢 Developers",  f"{int(kpi['total_developers']):,}"),
    (c6, "⭐ Avg Rating",  f"{kpi['avg_rating']}/5"),
]
for col, label, value in cards:
    with col:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "🎮 Game Performance",
    "💰 Revenue Analytics",
    "🏢 Developer Insights",
    "🏆 Top Games Leaderboard",
])

# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — Game Performance
# ──────────────────────────────────────────────────────────────────────────────

with tab1:
    st.subheader("🎮 Game Performance")

    gp = query(f"""
        SELECT gp.title, gp.total_sales, gp.total_revenue,
               gp.avg_rating, gp.total_reviews, gp.total_playtime,
               g.genre_name, p.platform_name
        FROM game_performance gp
        JOIN games ga ON gp.game_id = ga.game_id
        JOIN genres g ON ga.genre_id = g.genre_id
        JOIN platforms p ON ga.platform_id = p.platform_id
        WHERE g.genre_name = ANY(%s)
          AND p.platform_name = ANY(%s)
        ORDER BY gp.total_revenue DESC
        LIMIT {top_n}
    """, params=(sel_genres, sel_plats))

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("**Revenue by Game**")
        if not gp.empty:
            fig = px.bar(
                gp, x="total_revenue", y="title", orientation="h",
                color="avg_rating", color_continuous_scale="Viridis",
                labels={"total_revenue": "Revenue ($)", "title": "", "avg_rating": "Rating"},
            )
            fig.update_layout(**PLOT_LAYOUT)
            fig.update_yaxes(categoryorder="total ascending", gridcolor="#2d2d4e")
            fig.update_coloraxes(colorbar=dict(tickfont=dict(color="#e0e0e0")))
            st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("**Rating vs Revenue**")
        if not gp.empty:
            fig2 = px.scatter(
                gp, x="avg_rating", y="total_revenue",
                size="total_sales", color="genre_name",
                hover_name="title",
                labels={"avg_rating": "Avg Rating", "total_revenue": "Revenue ($)", "genre_name": "Genre"},
            )
            fig2.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Full Table**")
    st.dataframe(gp, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — Revenue Analytics
# ──────────────────────────────────────────────────────────────────────────────

with tab2:
    st.subheader("💰 Revenue Analytics")

    rg = query("""
        SELECT genre_name, total_games, total_sales, total_revenue, avg_rating
        FROM revenue_by_genre
        ORDER BY total_revenue DESC
    """)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("**Revenue by Genre**")
        fig = px.bar(
            rg, x="genre_name", y="total_revenue",
            color="avg_rating", color_continuous_scale="Plasma",
            labels={"genre_name": "Genre", "total_revenue": "Revenue ($)", "avg_rating": "Rating"},
        )
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("**Revenue Share by Genre**")
        fig2 = px.pie(
            rg, names="genre_name", values="total_revenue",
            hole=0.4, color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e0e0e0")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Revenue by Platform**")
    plat_rev = query("""
        SELECT p.platform_name, COUNT(DISTINCT g.game_id) AS total_games,
               COALESCE(ROUND(SUM(pu.amount_paid)::numeric, 2), 0) AS total_revenue
        FROM platforms p
        JOIN games g ON p.platform_id = g.platform_id
        LEFT JOIN purchases pu ON g.game_id = pu.game_id
        GROUP BY p.platform_name
        ORDER BY total_revenue DESC
        LIMIT 15
    """)
    fig3 = px.bar(
        plat_rev, x="platform_name", y="total_revenue",
        color="total_revenue", color_continuous_scale="Teal",
        labels={"platform_name": "Platform", "total_revenue": "Revenue ($)"},
    )
    fig3.update_layout(**PLOT_LAYOUT, coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("**Genre Table**")
    st.dataframe(rg, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 — Developer Insights
# ──────────────────────────────────────────────────────────────────────────────

with tab3:
    st.subheader("🏢 Developer Insights")

    dev = query(f"""
        SELECT developer_name, total_games, total_revenue, avg_rating
        FROM developer_performance
        ORDER BY total_revenue DESC
        LIMIT {top_n}
    """)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("**Top Developers by Revenue**")
        fig = px.bar(
            dev, x="total_revenue", y="developer_name", orientation="h",
            color="avg_rating", color_continuous_scale="Turbo",
            labels={"total_revenue": "Revenue ($)", "developer_name": "", "avg_rating": "Rating"},
        )
        fig.update_layout(**PLOT_LAYOUT)
        fig.update_yaxes(categoryorder="total ascending", gridcolor="#2d2d4e")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("**Games Count vs Revenue**")
        fig2 = px.scatter(
            dev, x="total_games", y="total_revenue",
            size="total_revenue", color="avg_rating",
            hover_name="developer_name",
            color_continuous_scale="RdYlGn",
            labels={"total_games": "# Games", "total_revenue": "Revenue ($)", "avg_rating": "Avg Rating"},
        )
        fig2.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Developer Table**")
    st.dataframe(dev, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 4 — Top Games Leaderboard
# ──────────────────────────────────────────────────────────────────────────────

with tab4:
    st.subheader("🏆 Top Games Leaderboard")

    sort_by = st.selectbox("Sort by", ["total_revenue", "avg_rating", "total_purchases", "global_sales"])

    tg = query(f"""
        SELECT title, developer_name, genre_name, platform_name,
               global_sales, total_revenue, avg_rating, total_purchases
        FROM top_games
        WHERE genre_name = ANY(%s)
          AND platform_name = ANY(%s)
        ORDER BY {sort_by} DESC
        LIMIT {top_n}
    """, params=(sel_genres, sel_plats))

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown(f"**Top {top_n} by {sort_by.replace('_', ' ').title()}**")
        fig = px.bar(
            tg, x=sort_by, y="title", orientation="h",
            color="genre_name",
            color_discrete_sequence=px.colors.qualitative.Bold,
            labels={sort_by: sort_by.replace("_", " ").title(), "title": "", "genre_name": "Genre"},
        )
        fig.update_layout(**PLOT_LAYOUT)
        fig.update_yaxes(categoryorder="total ascending", gridcolor="#2d2d4e")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("**Global Sales vs Revenue**")
        fig2 = px.scatter(
            tg, x="global_sales", y="total_revenue",
            size="total_purchases", color="genre_name",
            hover_name="title",
            color_discrete_sequence=px.colors.qualitative.Bold,
            labels={"global_sales": "Global Sales (M)", "total_revenue": "Revenue ($)", "genre_name": "Genre"},
        )
        fig2.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Leaderboard Table**")
    st.dataframe(tg, use_container_width=True, hide_index=True)

# ─── Footer ───────────────────────────────────────────────────────────────────

st.divider()
st.markdown(
    "<div style='text-align:center; color:#4a5568; font-size:0.8rem;'>"
    "GamePulse · PostgreSQL + Streamlit + Plotly"
    "</div>",
    unsafe_allow_html=True,
)
>>>>>>> 1477db6
