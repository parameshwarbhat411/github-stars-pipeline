SELECT DISTINCT repo_id,
    repo_name
FROM {{ ref('stg_gharchive') }}
