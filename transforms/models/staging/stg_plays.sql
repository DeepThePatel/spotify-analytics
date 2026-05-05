SELECT
    played_at::TIMESTAMP                          AS played_at,
    track_id,
    track_name,
    artist_name,
    artist_id,
    album_name,
    ROUND(duration_ms / 60000.0, 2)              AS duration_minutes,
    popularity,
    DATE(played_at::TIMESTAMP)                    AS played_date,
    HOUR(played_at::TIMESTAMP)                    AS played_hour,
    DAYOFWEEK(played_at::TIMESTAMP)               AS played_dow
FROM {{ source('spotify', 'raw_plays') }}