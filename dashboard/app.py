import streamlit as st
import duckdb
import plotly.express as px

con = duckdb.connect("data/spotify.duckdb")

st.title("My Spotify Listening History")

# --- top artists ---
st.subheader("Top Artists")
top_artists = con.execute("SELECT * FROM top_artists LIMIT 20").df()
fig = px.bar(
    top_artists,
    x="play_count",
    y="artist_name",
    orientation="h",
    labels={"play_count": "Plays", "artist_name": "Artist"},
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)

# --- listening by hour ---
st.subheader("When Do You Listen?")
by_hour = con.execute("SELECT * FROM listening_by_hour").df()
fig2 = px.bar(
    by_hour,
    x="played_hour",
    y="play_count",
    labels={"played_hour": "Hour of day", "play_count": "Plays"},
)
st.plotly_chart(fig2, use_container_width=True)

# --- listening by day ---
st.subheader("Plays Over Time")
by_day = con.execute("SELECT * FROM listening_by_day").df()
fig3 = px.line(
    by_day,
    x="played_date",
    y="play_count",
    labels={"played_date": "Date", "play_count": "Plays"},
)
st.plotly_chart(fig3, use_container_width=True)

# --- raw stats ---
st.subheader("Quick Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Total Tracks", con.execute("SELECT COUNT(*) FROM raw_plays").fetchone()[0])
col2.metric("Unique Artists", con.execute("SELECT COUNT(DISTINCT artist_name) FROM raw_plays").fetchone()[0])
col3.metric("Total Minutes", round(con.execute("SELECT SUM(duration_minutes) FROM stg_plays").fetchone()[0]))

con.close()