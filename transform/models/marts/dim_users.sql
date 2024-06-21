SELECT
    DISTINCT user as user_name
FROM
    {{ ref('stg_gharchive') }}