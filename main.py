# ingestion/fetch_history.py
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import duckdb
from datetime import datetime

load_dotenv()

# 1. Auth — you'll get these from developer.spotify.com (free)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-recently-played"
))

# 2. Pull last 50 tracks (Spotify's max per call)
results = sp.current_user_recently_played(limit=50)

# 3. Flatten to rows
rows = []
for item in results["items"]:
    track = item.get("track") or {}
    artists = track.get("artists") or []
    first_artist = artists[0] if artists else {}
    rows.append({
        "played_at": item.get("played_at"),
        "track_id": track.get("id"),
        "track_name": track.get("name"),
        "artist_name": first_artist.get("name"),
        "artist_id": first_artist.get("id"),
        "album_name": (track.get("album") or {}).get("name"),
        "duration_ms": track.get("duration_ms") or 0,
        "popularity": track.get("popularity") or 0,
    })

# 4. Load into DuckDB (creates file if it doesn't exist)
os.makedirs("data", exist_ok=True)
db_path = "data/spotify.duckdb"

try:
    con = duckdb.connect(db_path)
except duckdb.IOException:
    backup_path = f"{db_path}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.corrupt"
    os.replace(db_path, backup_path)
    print(f"Warning: invalid DuckDB file found. Backed up to {backup_path} and created a new database.")
    con = duckdb.connect(db_path)

con.execute("""
    CREATE TABLE IF NOT EXISTS raw_plays (
        played_at VARCHAR,
        track_id VARCHAR,
        track_name VARCHAR,
        artist_name VARCHAR,
        artist_id VARCHAR,
        album_name VARCHAR,
        duration_ms INTEGER,
        popularity INTEGER,
        ingested_at TIMESTAMP DEFAULT current_timestamp
    )
""")

# Insert only new rows (dedup on played_at)
con.executemany("""
    INSERT INTO raw_plays (played_at, track_id, track_name, artist_name,
                           artist_id, album_name, duration_ms, popularity)
    SELECT ?, ?, ?, ?, ?, ?, ?, ?
    WHERE NOT EXISTS (
        SELECT 1 FROM raw_plays WHERE played_at = ?
    )
""", [(r["played_at"], r["track_id"], r["track_name"], r["artist_name"],
       r["artist_id"], r["album_name"], r["duration_ms"], r["popularity"],
       r["played_at"]) for r in rows])

print(f"Ingested up to {len(rows)} tracks. Total in DB: {con.execute('SELECT COUNT(*) FROM raw_plays').fetchone()[0]}")
con.close()