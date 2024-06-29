{% macro fact_event_type_weekly(fact_table, event_count, eventCount, last_week_event_count) %}

WITH repo_date_range AS (
  SELECT
    repo_id,
    MIN(event_date) AS min_date,
    MAX(event_date) AS max_date
  FROM {{ ref(fact_table) }}
  GROUP BY 1
), repo_week_spine AS (
  SELECT
    rd.repo_id,
    d.date_week
  FROM dim_date_week AS d
  JOIN repo_date_range AS rd
    ON d.date_week BETWEEN DATE_TRUNC('week', rd.min_date) AND DATE_TRUNC('week', rd.max_date)
), aligned_fact_stars AS (
  SELECT
    DATE_TRUNC('week', event_date) AS date_week,
    repo_id,
    COUNT(*) AS {{ event_count }}
  FROM {{ ref(fact_table) }}
  GROUP BY 1, 2
)

SELECT
  rws.date_week,
  rws.repo_id,
  COALESCE(afs.{{ event_count }}, 0) AS {{ eventCount }},
  LAG({{ eventCount }}) OVER (PARTITION BY rws.repo_id ORDER BY rws.date_week) AS {{ last_week_event_count }},
  COALESCE(({{ eventCount }} / NULLIF({{ last_week_event_count }}, 0)) - 1, 1) AS wow_growth
FROM repo_week_spine AS rws
LEFT JOIN aligned_fact_stars AS afs
  ON rws.date_week = afs.date_week + INTERVAL 1 DAY
  AND rws.repo_id = afs.repo_id
ORDER BY rws.repo_id, rws.date_week

{% endmacro %}