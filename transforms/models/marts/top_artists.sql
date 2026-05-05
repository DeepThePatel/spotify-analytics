SELECT
    artist_name,
    artist_id,
    COUNT(*)                                      AS play_count,
    ROUND(SUM(duration_minutes), 1)               AS total_minutes,
    ROUND(AVG(popularity), 1)                     AS avg_popularity
FROM {{ ref('stg_plays') }}
GROUP BY artist_name, artist_id
ORDER BY play_count DESC