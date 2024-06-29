{% macro fact_event_type_monthly(fact_table, event_count, last_year_event_count) %}

WITH repo_date_range AS (
  SELECT
    repo_id,
    MIN(event_date) AS min_date,
    MAX(event_date) AS max_date
  FROM {{ ref(fact_table)}}
  GROUP BY 1
),

repo_month_spine AS (
  SELECT
    rd.repo_id,
    d.date_month
  FROM {{ ref("dim_date_month") }} AS d
  JOIN repo_date_range AS rd
    ON d.date_month
    BETWEEN DATE_TRUNC('month', rd.min_date)
    AND DATE_TRUNC('month', rd.max_date)
)

SELECT
  rm.date_month,
  rm.repo_id,
  SUM(CASE WHEN s.event_date IS NULL THEN 0 ELSE 1 END) AS {{ event_count }},
  LAG({{ event_count }}, 12) OVER (PARTITION BY rm.repo_id ORDER BY rm.date_month) AS {{ last_year_event_count }},
 IFNULL( ({{ event_count }} / {{ last_year_event_count }}) - 1 , 1) AS yoy_growth
FROM repo_month_spine AS rm
  LEFT JOIN {{ ref(fact_table) }} AS s
  ON rm.date_month = date_trunc('month', s.event_date)
  AND rm.repo_id = s.repo_id
GROUP BY 1, 2

{% endmacro %}