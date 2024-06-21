{{ config(materialized='incremental') }}

-- CTE to get the max loaded_at value
WITH max_loaded AS (
    SELECT MAX(event_loaded_date) AS max_loaded_at
    FROM {{ this }}
)

-- Main query
SELECT
    CASE
        WHEN type = 'Event' THEN type
        ELSE REPLACE(type, 'Event', '')
    END AS event_type,
    actor.login AS "user",
    repo.id AS repo_id,
    repo.name AS repo_name,
    created_at AS event_date,
    loaded_at AS event_loaded_date
FROM {{ source('gharchive', 'src_gharchive') }}
{% if is_incremental() %}
WHERE loaded_at > (SELECT max_loaded_at FROM max_loaded)
{% endif %}