{% macro fact_event_type(event_type) %}
SELECT
    stg.event_date AS event_date,
    dr.repo_id,
    du.user_name
FROM
    {{ ref('stg_gharchive') }} as stg
JOIN
    {{ ref('dim_repos') }} dr
ON
    stg.repo_id = dr.repo_id
    AND stg.event_date >= dr.start_date
    AND (stg.event_date < dr.end_date OR dr.end_date IS NULL)
JOIN
    {{ ref('dim_users') }} du
ON
    stg.user = du.user_name
WHERE
    stg.event_type = '{{ event_type }}'

{% endmacro %}