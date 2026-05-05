SELECT
    played_hour,
    COUNT(*)                                      AS play_count,
    ROUND(SUM(duration_minutes), 1)               AS total_minutes
FROM {{ ref('stg_plays') }}
GROUP BY played_hour
ORDER BY played_hour