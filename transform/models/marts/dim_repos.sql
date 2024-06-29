SELECT DISTINCT repo_id,
    repo_name,
    MIN(event_date) as start_date,
    LEAD(start_date) OVER(PARTITION BY repo_id ORDER BY start_date) as end_date
FROM {{ ref('stg_gharchive') }}
GROUP BY 1,2
ORDER BY 1,3