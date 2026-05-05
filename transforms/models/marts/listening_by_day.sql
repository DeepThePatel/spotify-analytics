SELECT
    played_date,
    COUNT(*)                                      AS play_count,
    ROUND(SUM(duration_minutes), 1)               AS total_minutes
FROM {{ ref('stg_plays') }}
GROUP BY played_date
ORDER BY played_date